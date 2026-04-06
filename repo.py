import json
import os
import uuid
import numpy as np
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity

from langchain_openai import OpenAIEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage



from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


# QA System for Medical Reports using LangChain
class ReportQASystem:
    def __init__(self, api_key=None):  # Fixed: __init__ instead of _init_
        self.api_key = api_key
        self.conversation_history = []
        self.analysis_store = self.load_analysis_store()

        if self.api_key:
            self.llm = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo", temperature=0.3)
            self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        else:
            self.llm = None
            self.embeddings = None

    def load_analysis_store(self):
        if os.path.exists("analysis_store.json"):
            with open("analysis_store.json", "r") as f:
                return json.load(f)
        return {"analyses": []}

    def get_embeddings(self, text):
        if self.embeddings:
            try:
                return self.embeddings.embed_query(text)
            except Exception as e:
                print(f"Embedding error: {e}")
        return np.random.rand(1536)

    def get_relevant_contexts(self, query, top_k=3):
        query_embedding = self.get_embeddings(query)
        analyses = self.analysis_store["analyses"]
        if not analyses:
            return ["No previous analyses found."]

        contexts = []
        for analysis in analyses:
            analysis_text = analysis.get("analysis", "")
            if not analysis_text.strip():
                continue

            full_text = analysis_text
            if "findings" in analysis and analysis["findings"]:
                findings_text = "\n".join([f"- {finding}" for finding in analysis["findings"]])
                full_text += f"\n\nFindings:\n{findings_text}"

            full_text += f"\n\nImage: {analysis.get('filename', 'unknown')}"
            full_text += f"\nDate: {analysis.get('date', '')[:10]}"

            contexts.append({
                "text": full_text,
                "embedding": self.get_embeddings(full_text),
                "id": analysis.get("id", ""),
                "date": analysis.get("date", "")
            })

        similarities = [
            (cosine_similarity([query_embedding], [c["embedding"]])[0][0], c) for c in contexts
        ]
        similarities.sort(reverse=True)
        return [c["text"] for _, c in similarities[:top_k]]

    def answer_question(self, question):
        if not self.llm:
            return "Please provide a valid OpenAI API key."

        contexts = self.get_relevant_contexts(question)
        if not contexts or contexts[0] == "No previous analyses found.":
            return "No prior analyses available. Please upload and analyze images first."

        combined_context = "\n\n---\n\n".join(contexts)
        self.conversation_history.append(HumanMessage(content=question))

        system_prompt = f"""You are a medical AI assistant answering questions about medical reports.
Use the following contexts to answer the question. If not enough information is available, say so and suggest what else is needed.

Contexts:
{combined_context}
"""

        messages = [SystemMessage(content=system_prompt)] + self.conversation_history

        try:
            response = self.llm(messages)
            self.conversation_history.append(response)

            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]

            return response.content
        except Exception as e:
            return f"Error during LLM response: {str(e)}"

    def clear_history(self):
        self.conversation_history = []
        return "Conversation history cleared."


# Chat room system for QA using ReportQASystem
class ReportQAChat:
    def __init__(self, qa_system):  # Fixed: __init__ instead of _init_
        self.qa_system = qa_system
        self.qa_chat_store = self.get_qa_chat_store()

    def get_qa_chat_store(self):
        if os.path.exists("qa_chat_store.json"):
            with open("qa_chat_store.json", "r") as f:
                return json.load(f)
        return {"rooms": {}}

    def save_qa_chat_store(self):
        with open("qa_chat_store.json", "w") as f:
            json.dump(self.qa_chat_store, f, indent=2)

    def create_qa_room(self, user_name, room_name):
        room_id = f"QA-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        room_data = {
            "id": room_id,
            "name": room_name,
            "created_at": datetime.now().isoformat(),
            "creator": user_name,
            "messages": []
        }

        welcome_message = {
            "id": str(uuid.uuid4()),
            "user": "System",
            "content": f"Welcome {user_name}! You can ask questions about your reports in the room '{room_name}'.",
            "timestamp": datetime.now().isoformat()
        }

        room_data["messages"].append(welcome_message)
        self.qa_chat_store["rooms"][room_id] = room_data
        self.save_qa_chat_store()
        return room_id

    def add_message(self, room_id, user_name, message):
        if room_id not in self.qa_chat_store["rooms"]:
            return None

        user_msg = {
            "id": str(uuid.uuid4()),
            "user": user_name,
            "content": message,
            "timestamp": datetime.now().isoformat()
        }

        # Get assistant reply using LangChain-powered system
        assistant_reply = self.qa_system.answer_question(message)

        assistant_msg = {
            "id": str(uuid.uuid4()),
            "user": "AI Assistant",
            "content": assistant_reply,
            "timestamp": datetime.now().isoformat()
        }

        self.qa_chat_store["rooms"][room_id]["messages"].extend([user_msg, assistant_msg])
        self.save_qa_chat_store()
        return [user_msg, assistant_msg]

    def get_messages(self, room_id, limit=50):
        if room_id not in self.qa_chat_store["rooms"]:
            return []
        messages = self.qa_chat_store["rooms"][room_id]["messages"]
        return messages[-limit:] if len(messages) > limit else messages

    def get_qa_rooms(self):
        rooms = []
        for room_id, room_data in self.qa_chat_store["rooms"].items():
            rooms.append({
                "id": room_id,
                "name": room_data.get("name", "Unnamed Room"),
                "creator": room_data.get("creator", "Unknown"),
                "created_at": room_data.get("created_at", "")
            })
        rooms.sort(key=lambda x: x["created_at"], reverse=True)
        return rooms

    def delete_qa_room(self, room_id):
        if room_id in self.qa_chat_store["rooms"]:
            del self.qa_chat_store["rooms"][room_id]
            self.save_qa_chat_store()
            return True
        return False
      
