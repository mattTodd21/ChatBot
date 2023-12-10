import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit
from nltk.chat.util import Chat, reflections

# Chatbot logic
pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, how are you today?", "Nice to meet you %1, how can I assist you?", "Pleased to meet you %1, how's your day going?"]
    ],
    [
        r"hi|hello|hey|good morning|good afternoon",
        ["Hello", "Hey there", "Hi there! How can I assist you today?", "Hello! How can I help you?", "Good day! What can I do for you?"]
    ],
    [
        r"what is your name ?",
        ["I am a simple chatbot, you can call me Chatbot.", "I'm Chatbot, here to assist you.", "Call me Chatbot, your virtual assistant."]
    ],
    [
        r"how are you ?",
        ["I'm doing good, thank you. How can I assist you?", "I'm fine, thanks for asking. How about you?", "I'm as good as a bot can be! What about you?"]
    ],
    [
        r"sorry (.*)",
        ["It's alright", "It's OK, don't worry about it", "No problem, how can I assist you further?", "That's okay, everyone makes mistakes."]
    ],
    [
        r"i'm (.*) (good|well|okay|ok)",
        ["Great to hear that! How can I assist you today?", "Good to know! Do you have any questions for me?", "That's good to hear. What can I do for you today?"]
    ],
    [
        r"what (.*) doing ?",
        ["I'm chatting with you at the moment. How can I assist?", "Right now, I'm here to help you. Have any questions?", "I'm here, ready to answer your questions!"]
    ],
    [
        r"how (.*) weather in (.*)?",
        ["I'm not sure about the current weather in %2, but I recommend checking a reliable weather site.", "Weather in %2? I suggest looking at a weather forecast for the most accurate information."]
    ],
    [
        r"i work in (.*)",
        ["%1 is an interesting field. What's your role there?", "%1 sounds challenging. What do you do there?", "Working in %1 must be exciting. Can you tell me more about your work?"]
    ],
    [
        r"i like (.*)",
        ["%1 is quite interesting. What attracts you to it?", "%1 sounds fascinating. Can you tell me more?", "That's cool. What do you like most about %1?"]
    ],
    [
        r"i feel (.*)",
        ["Why do you feel %1? Sometimes, discussing it can be helpful.", "Feeling %1 is quite natural. Would you like to talk about it?", "It's okay to feel %1. Do you want to discuss it?"]
    ],
    [
        r"(.*) (movie|film|show)?",
        ["I don't watch movies, but I can discuss them! What's your favorite?", "I'm not able to watch shows, but I'd love to hear about your favorites.", "While I can't watch films, I can certainly talk about them. What genres do you like?"]
    ],
    [
        r"who is your favorite (actor|actress)?",
        ["As a bot, I don't have favorites, but I can find information on actors for you!", "I don't have personal tastes, but I can look up info on any actor or actress.", "Favorite actors? I don't have one, but I can help you find info about them."]
    ],
    [
        r"tell me a joke",
        ["Why don't scientists trust atoms? Because they make up everything!", "Why was the math book sad? It had too many problems.", "What do you call a fake noodle? An Impasta!"]
    ],
    [
        r"(.*) sport?",
        ["I don't play sports, but I can provide info about them. What's your favorite?", "Sports aren't my thing, but I can find sports news for you. Which sport interests you?", "I'm not into sports, but I can look up sports information. What are you interested in?"]
    ],
    [
        r"give me some advice",
        ["Remember to take breaks and care for your wellbeing.", "Stay curious and keep learning new things!", "Be kind to yourself and others. What else can I assist with?"]
    ],
    [
        r"bye|exit|goodbye",
        ["Goodbye! Don't hesitate to return if you have more questions.", "It was nice chatting with you. Have a great day!", "Farewell! Feel free to come back if you need assistance."]
    ],
    [
        r"(.*) music?",
        ["I can't listen to music, but I can discuss it. What's your favorite genre?", "Music is fascinating. What type of music do you enjoy?", "Though I can't hear music, I'm curious about your preferences. What do you like to listen to?"]
    ],
    [
        r"i need help with (.*)",
        ["Sure, I can help with %1. What specifically do you need assistance with?", "%1, got it. What do you need to know?", "I'm here to help with %1. Please tell me more about your issue."]
    ],
    [
        r"do you know (.*)",
        ["I might know about %1, what do you want to know?", "I have access to a lot of information, including about %1. What's your question?", "I might be able to help with %1. What are you curious about?"]
    ],
    [
        r"what (.*) you recommend ?",
        ["I'm not capable of personal opinions, but I can look up popular recommendations on %1.", "For %1, I would suggest checking out some expert reviews.", "While I can't give personal recommendations, I can find highly rated options for %1."]
    ],
    [
        r"(.*) (book|novel)?",
        ["I don't read books, but I can discuss them. What's your favorite book?", "Books are a treasure trove of knowledge. Do you have a favorite?", "While I can't read, I can certainly talk about books. What genre do you like?"]
    ],
    [
        r"(.*) (difficult|hard)",
        ["Sometimes, %1 can be challenging. What specifically are you finding hard?", "%1 can be tough, but I'm here to help. Can you tell me more?", "Dealing with %1 can be demanding. How can I assist you with it?"]
    ],
    [
        r"(.*) (happy|pleased|excited)",
        ["It's great to hear you're feeling %1! What's making you feel this way?", "Feeling %1 is wonderful. What's the reason for your happiness?", "%1 is a great feeling. What's been going well?"]
    ],
    [
        r"(.*) sad|unhappy|depressed",
        ["I'm sorry to hear you're feeling %1. Do you want to talk about it?", "Feeling %1 can be tough. I'm here if you need to discuss anything.", "It's okay to feel %1. Talking about it can sometimes help. What's on your mind?"]
    ],
    [
        r"(.*) (hungry|eat|food)",
        ["If you're hungry, maybe it's time to take a break and grab a bite!", "Thinking about food? What's your favorite meal?", "Food is essential. What do you feel like eating?"]
    ],
    [
        r"(.*) (tired|sleepy)",
        ["Feeling tired can be a sign to rest. Are you getting enough sleep?", "If you're sleepy, taking a short break might help recharge.", "It's important to rest when you're tired. Do you need to adjust your sleep schedule?"]
    ],
    [
        r"(.*) (bored|boring)",
        ["Boredom can be a sign to try something new. Any hobbies you're interested in?", "If you're feeling bored, maybe explore a new interest or hobby.", "When things get boring, it's a good chance to experiment with new activities."]
    ],
    [
        r"i'm worried about (.*)",
        ["Worrying about %1 is natural. Would you like to discuss it more?", "Concerns about %1 are understandable. How can I assist?", "It's okay to be worried about %1. Talking about it might help."]
    ],
    [
        r"what (.*) mean?",
        ["%1 can mean different things depending on the context. Can you provide more details?", "The meaning of %1 varies. Could you elaborate a bit more?", "%1 has multiple meanings. What context are you referring to?"]
    ],
    [
        r"(.*) (funny|humorous)",
        ["Humor is a great way to lighten the mood. Have you heard any good jokes about %1?", "Finding humor in %1 can be delightful. Know any related jokes?", "%1 can be funny indeed. Do you have any humorous anecdotes related to it?"]
    ],
    [
        r"tell me about (.*)",
        ["What would you like to know about %1?", "There's a lot to say about %1. Any specific questions?", "%1 is a broad topic. Can you narrow it down a bit?"]
    ],
    [
        r"(.*) (annoying|frustrating)",
        ["Dealing with %1 can be challenging. What exactly is troubling you?", "It's normal to find %1 annoying. Want to talk about it?", "%1 can be frustrating. How are you managing it?"]
    ],
    [
        r"can you help with (.*)",
        ["I can try to help with %1. What do you need assistance with?", "I'll do my best to assist with %1. What's your question?", "Helping with %1 is within my capabilities. What do you need to know?"]
    ],
    [
        r"(.*) (love|relationship)",
        ["Love and relationships are complex. What are your thoughts on %1?", "Relationships and %1 can be intricate. Do you have specific concerns?", "Discussing %1 can be insightful. What's on your mind about it?"]
    ],
    [
        r"i'm thinking about (.*)",
        ["Thinking about %1 is interesting. What are your thoughts on it?", "%1 can be thought-provoking. What perspective do you have?", "Reflecting on %1 is a good exercise. What conclusions have you reached?"]
    ],
    [
        r"how to (.*)",
        ["To %1, there are usually several methods. What have you tried so far?", "There are different ways to %1. What's your specific goal?", "Achieving %1 can be done in various ways. What approach are you considering?"]
    ],
    [
        r"your (.*) favorite?",
        ["As a bot, I don't have favorites, but I can find popular choices in %1.", "Favorites don't apply to me, but I can provide information on common preferences in %1.", "I don't have personal favorites, but I can tell you what's popular in %1."]
    ],
    [
        r"i am (confused|unsure) about (.*)",
        ["Being unsure about %2 is normal. How can I clarify it for you?", "Confusion about %2 is common. What are your specific questions?", "Understanding %2 can be tricky. What aspects are you struggling with?"]
    ],
    [
        r"can you explain (.*)",
        ["I can certainly try to explain %1. What are you curious about?", "Explaining %1 is within my capabilities. What do you need to know?", "I'll do my best to explain %1. What specifics are you looking for?"]
    ],
    [
        r"(.*) (fun|entertaining)",
        ["Finding fun in %1 is great. What do you enjoy about it?", "%1 can be very entertaining. What aspects do you find most enjoyable?", "Enjoying %1 is wonderful. What makes it fun for you?"]
    ],
    [
        r"i am (happy|glad) to (.*)",
        ["It's good to hear that you're happy to %2. What brings you this joy?", "Being glad to %2 is a positive attitude. What motivates you in it?", "Your happiness in %2 is great. What's the best part about it for you?"]
    ],
    [
        r"can you recommend (.*)",
        ["I can suggest options for %1 based on popular choices.", "For %1, I can look up recommendations. Any specific criteria?", "I can find recommendations for %1. What are you looking for specifically?"]
    ],
    [
        r"how (.*) works?",
        ["%1 works through a specific process. What details are you interested in?", "The workings of %1 can be complex. What part do you want to know about?", "%1's functionality is intricate. What aspect are you curious about?"]
    ],
    [
        r"i want to learn (.*)",
        ["Learning %1 is a great goal. Where are you planning to start?", "Pursuing knowledge in %1 is commendable. What resources do you have?", "To learn %1, there are many paths. What approach are you considering?"]
    ],
    [
        r"(.*) (difficult|hard) to learn",
        ["Learning %1 can be challenging. What difficulties are you facing?", "%1 can be tough to grasp. What areas are you struggling with?", "Mastering %1 takes time and effort. How can I assist your learning process?"]
    ],
    [
        r"i don't like (.*)",
        ["Disliking %1 is understandable. What don't you like about it?", "Preferences vary, and that's okay. What turns you off about %1?", "Not everyone likes %1, and that's fine. What's your reason?"]
    ],
]

chatbot = Chat(pairs, reflections)

class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.username = None

    def initUI(self):
        # Layout
        layout = QVBoxLayout()

        # Username Entry
        self.usernameEntry = QLineEdit()
        self.usernameEntry.setPlaceholderText("Enter your username")
        self.usernameEntry.returnPressed.connect(self.set_username)
        layout.addWidget(self.usernameEntry)

        # Text Edit
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        layout.addWidget(self.textEdit)

        # Text Entry
        self.textEntry = QLineEdit()
        self.textEntry.returnPressed.connect(self.onEnter)
        layout.addWidget(self.textEntry)

        # Feedback Buttons
        self.helpfulButton = QPushButton('Helpful')
        self.helpfulButton.clicked.connect(self.feedback_helpful)
        layout.addWidget(self.helpfulButton)

        self.notHelpfulButton = QPushButton('Not Helpful')
        self.notHelpfulButton.clicked.connect(self.feedback_not_helpful)
        layout.addWidget(self.notHelpfulButton)

        # Set layout
        self.setLayout(layout)

        # Window settings
        self.setWindowTitle('Chatbot')
        self.setGeometry(300, 300, 350, 250)

    def set_username(self):
        self.username = self.usernameEntry.text()
        self.textEdit.append(f"Welcome, {self.username}!")
        self.usernameEntry.setDisabled(True)
        self.load_user_data()

    def load_user_data(self):
        if self.username:
            try:
                with open(f'{self.username}_data.txt', 'r') as file:
                    user_data = file.read()
                    self.textEdit.append(f"Welcome back, {self.username}! Last time we talked about: {user_data}")
            except FileNotFoundError:
                self.textEdit.append("Looks like you're new here. Let's chat!")

    def onEnter(self):
        user_input = self.textEntry.text()
        bot_response = chatbot.respond(user_input)
        self.textEdit.append("You: " + user_input)
        self.textEdit.append("Bot: " + bot_response)
        self.textEntry.clear()
        self.store_user_data(user_input)

    def store_user_data(self, user_input):
        if self.username:
            with open(f'{self.username}_data.txt', 'a') as file:
                file.write(f'{user_input}\n')

    def feedback_helpful(self):
        self.store_feedback(True)

    def feedback_not_helpful(self):
        self.store_feedback(False)

    def store_feedback(self, was_helpful):
        if self.username:
            with open('feedback_data.txt', 'a') as file:
                file.write(f'{self.username}|{was_helpful}\n')

def main():
    app = QApplication(sys.argv)
    chat_window = ChatWindow()
    chat_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
