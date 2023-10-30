class ChatHistory:
    def __init__(self):
        self.chats = []
        self.current_chat = []
        self.titles = []

    def new_chat(self, title):
        if self.current_chat:
            self.chats.append(self.current_chat)
            self.titles.append("You: " + self.current_chat[0]['user'] + "\nClaude2: " + self.current_chat[0]['claude2'])
        self.current_chat = []

    def add_message(self, user_message, claude2_response):
        self.current_chat.append({
            "user": user_message,
            "claude2": claude2_response
        })

    def save_chat(self):
        if self.current_chat:
            self.chats.append(self.current_chat)
            self.current_chat = []

    def get_chats(self):
        return self.chats

    def get_messages(self):
        return self.current_chat

    def get_titles(self):
        return self.titles