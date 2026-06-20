# ============================================
# AI Chatbot with Natural Language Processing
# Author: Muhammad Sohaib Imran
# FAST-NUCES, Lahore | FinTech
# Install: pip install nltk
# ============================================

import random
import re
import os
from datetime import datetime

# ─── KNOWLEDGE BASE ───────────────────────────────────────────

INTENTS = {
    "greeting": {
        "patterns": ["hello", "hi", "hey", "good morning", "good evening",
                     "good afternoon", "howdy", "whats up", "what's up", "sup"],
        "responses": [
            "Hey! 👋 I'm SohaibBot. How can I help you today?",
            "Hello! Great to see you. What's on your mind?",
            "Hi there! I'm here to help. Ask me anything!",
            "Hey! Ready to chat. What would you like to know?"
        ]
    },
    "farewell": {
        "patterns": ["bye", "goodbye", "see you", "later", "take care",
                     "exit", "quit", "cya", "peace", "farewell"],
        "responses": [
            "Goodbye! Have a great day! 👋",
            "See you later! Take care! 😊",
            "Bye! Come back anytime you need help!",
            "Take care! It was great chatting with you! 🌟"
        ]
    },
    "thanks": {
        "patterns": ["thank you", "thanks", "thank", "thx", "appreciate",
                     "helpful", "great help", "you're great"],
        "responses": [
            "You're welcome! 😊 Happy to help!",
            "Anytime! That's what I'm here for! 🌟",
            "Glad I could help! Let me know if you need anything else.",
            "My pleasure! Feel free to ask more questions!"
        ]
    },
    "identity": {
        "patterns": ["who are you", "what are you", "your name", "introduce yourself",
                     "tell me about yourself", "what can you do", "your purpose"],
        "responses": [
            "I'm SohaibBot 🤖 — an AI chatbot built by Muhammad Sohaib Imran, a FinTech student at FAST-NUCES Lahore. I can help with crypto, finance, coding, and general knowledge!",
            "I'm SohaibBot! Created by Muhammad Sohaib Imran as an AI project. I understand natural language and can answer questions about crypto, finance, and much more!",
        ]
    },
    "creator": {
        "patterns": ["who made you", "who created you", "who built you",
                     "who is your creator", "who programmed you", "who is sohaib"],
        "responses": [
            "I was built by Muhammad Sohaib Imran 👨‍💻 — a FinTech student at FAST-NUCES Lahore, Pakistan. He's a crypto trader, entrepreneur, and AI enthusiast!",
            "My creator is Muhammad Sohaib Imran — a passionate FinTech student, 6-year crypto trader, and entrepreneur from Lahore, Pakistan! 🇵🇰"
        ]
    },
    "crypto_general": {
        "patterns": ["what is crypto", "what is cryptocurrency", "explain crypto",
                     "how does crypto work", "what is blockchain", "tell me about crypto"],
        "responses": [
            "Cryptocurrency 💰 is a digital or virtual currency secured by cryptography, making it nearly impossible to counterfeit. It operates on decentralized networks using blockchain technology — a distributed ledger that records all transactions across thousands of computers.",
            "Crypto is digital money that uses blockchain technology. Unlike traditional currencies, it's decentralized — meaning no bank or government controls it. Bitcoin was the first cryptocurrency, created in 2009 by the mysterious Satoshi Nakamoto! 🔗"
        ]
    },
    "bitcoin": {
        "patterns": ["what is bitcoin", "tell me about bitcoin", "bitcoin price",
                     "should i buy bitcoin", "btc", "bitcoin explain"],
        "responses": [
            "Bitcoin (BTC) ₿ is the world's first and most valuable cryptocurrency, created in 2009. It has a fixed supply of 21 million coins, making it deflationary. Many call it 'digital gold' as a store of value!",
            "Bitcoin is the king of crypto! 👑 It was created by the anonymous Satoshi Nakamoto in 2009. With a max supply of 21 million BTC, it's scarce by design. As a 6-year trader, I'd say always do your own research before investing!"
        ]
    },
    "ethereum": {
        "patterns": ["what is ethereum", "tell me about ethereum", "eth", "ethereum explain",
                     "smart contracts", "what are smart contracts"],
        "responses": [
            "Ethereum (ETH) is the second largest cryptocurrency and a programmable blockchain. It introduced smart contracts — self-executing code that runs when conditions are met. Most DeFi apps and NFTs are built on Ethereum! 🔷",
            "Ethereum is like a world computer! 💻 Unlike Bitcoin which is just digital money, Ethereum lets developers build decentralized apps (dApps) on it. Smart contracts automatically execute agreements without middlemen!"
        ]
    },
    "trading": {
        "patterns": ["how to trade crypto", "crypto trading tips", "trading advice",
                     "how to invest in crypto", "trading strategy", "when to buy",
                     "when to sell", "trading for beginners"],
        "responses": [
            "As someone who's been trading crypto for 6 years, here are my top tips 📈:\n  1. Never invest more than you can afford to lose\n  2. Always do your own research (DYOR)\n  3. Understand market cycles (bull/bear)\n  4. Use stop losses to protect capital\n  5. Don't let emotions drive decisions\n  6. Diversify your portfolio",
            "Crypto trading tips from 6 years of experience 🎯:\n  • Start small and learn the markets\n  • Study technical analysis (support/resistance, RSI, MACD)\n  • Never chase pumps\n  • Take profits along the way\n  • Long-term holding (HODLing) often beats short-term trading!"
        ]
    },
    "defi": {
        "patterns": ["what is defi", "decentralized finance", "defi explain",
                     "yield farming", "liquidity pool", "staking"],
        "responses": [
            "DeFi (Decentralized Finance) 🏦 is a financial system built on blockchain that operates without banks or intermediaries. You can lend, borrow, trade, and earn interest using smart contracts. Popular DeFi platforms include Uniswap, Aave, and Compound!",
            "DeFi is like a bank without the bank! 🔓 It uses smart contracts to offer financial services — lending, borrowing, earning interest (yield farming), and trading — all without needing permission from any institution. Very exciting space!"
        ]
    },
    "fintech": {
        "patterns": ["what is fintech", "fintech explain", "financial technology",
                     "fintech examples", "future of finance"],
        "responses": [
            "FinTech (Financial Technology) 💳 is the use of technology to improve and automate financial services. Examples include mobile banking apps (JazzCash, Easypaisa in Pakistan), crypto exchanges, robo-advisors, and AI-powered fraud detection!",
            "FinTech is transforming how we handle money! 🚀 It includes everything from mobile payments and digital banking to AI-driven investment platforms. As a FinTech student at FAST, I'm excited to be part of this revolution in Pakistan!"
        ]
    },
    "ai": {
        "patterns": ["what is ai", "artificial intelligence", "machine learning",
                     "deep learning", "explain ai", "future of ai", "ai in finance"],
        "responses": [
            "Artificial Intelligence (AI) 🤖 is the simulation of human intelligence by machines. It includes Machine Learning (systems that learn from data), Deep Learning (neural networks), and Natural Language Processing (understanding human language — like what I use!).",
            "AI is transforming every industry! 🌍 In finance, AI is used for fraud detection, algorithmic trading, credit scoring, and risk assessment. Combined with FinTech, AI is creating a smarter financial future. This is exactly why I'm passionate about AI + FinTech! 🚀"
        ]
    },
    "pakistan_tech": {
        "patterns": ["pakistan tech", "tech in pakistan", "netsol", "systems limited",
                     "pakistan software", "pakistan startups", "tech jobs pakistan"],
        "responses": [
            "Pakistan's tech industry is booming! 🇵🇰 Top companies include Netsol Technologies (global leader in leasing software), Systems Limited, Arbisoft, and Tintash. Pakistan exports over $2 billion in IT services annually!",
            "Pakistan has a thriving tech ecosystem! 💡 Netsol Technologies, based in Lahore, is listed on NASDAQ and serves clients in over 30 countries. Systems Limited is another giant. The future for Pakistani tech graduates is very bright! 🌟"
        ]
    },
    "time": {
        "patterns": ["what time is it", "current time", "what is the time", "time now"],
        "responses": []  # Dynamic response
    },
    "date": {
        "patterns": ["what date is it", "today's date", "what day is it", "current date"],
        "responses": []  # Dynamic response
    },
    "joke": {
        "patterns": ["tell me a joke", "joke", "make me laugh", "say something funny",
                     "funny", "humor"],
        "responses": [
            "Why do programmers prefer dark mode? Because light attracts bugs! 🐛😄",
            "Why did the crypto investor lose all his money? He kept buying high and selling low — and called it a 'strategy'! 😂",
            "A SQL query walks into a bar, walks up to two tables and asks... 'Can I join you?' 🍺😄",
            "Why don't scientists trust atoms? Because they make up everything! ⚛️😂",
            "How many programmers does it take to change a light bulb? None — that's a hardware problem! 💡😄"
        ]
    },
    "motivation": {
        "patterns": ["motivate me", "i need motivation", "inspire me", "feeling down",
                     "feeling lazy", "give me motivation", "i want to give up"],
        "responses": [
            "You've got this! 💪 Remember — every expert was once a beginner. Keep pushing forward, one day at a time!",
            "Success is not final, failure is not fatal — it's the courage to continue that counts! 🌟 Keep going!",
            "Think about why you started. Every line of code, every project, every late night is building your future empire! 🚀",
            "The best time to start was yesterday. The second best time is NOW! 🔥 Let's go!"
        ]
    },
    "math": {
        "patterns": ["calculate", "what is", "math", "plus", "minus", "multiply",
                     "divide", "sum", "addition", "subtraction"],
        "responses": []  # Dynamic - handled separately
    },
    "help": {
        "patterns": ["help", "what can you do", "commands", "features",
                     "how to use", "capabilities", "menu"],
        "responses": [
            """I can help you with: 📋
  🪙 Crypto — Bitcoin, Ethereum, DeFi, trading tips
  💹 Finance — FinTech, investing, markets
  🤖 AI & Tech — Artificial intelligence, machine learning
  🇵🇰 Pakistan Tech — Netsol, tech industry
  😄 Fun — Jokes, motivation, casual chat
  🧮 Math — Simple calculations
  ⏰ Time & Date — Current time and date
  
  Just type naturally and I'll understand you!"""
        ]
    },
    "unknown": {
        "patterns": [],
        "responses": [
            "Hmm, I'm not sure about that one! 🤔 Try asking about crypto, finance, AI, or tech!",
            "I didn't quite get that. Could you rephrase? Or type 'help' to see what I can do! 😊",
            "Interesting question! I'm still learning. Try asking about crypto, FinTech, or AI! 🤖",
            "That's beyond my current knowledge! Type 'help' to see what topics I cover. 📚"
        ]
    }
}


# ─── NLP ENGINE ───────────────────────────────────────────────

def preprocess(text):
    """Clean and normalize input text."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)
    return text


def detect_intent(user_input):
    """Detect user intent using pattern matching."""
    cleaned = preprocess(user_input)

    # Check for math expressions
    math_pattern = re.search(r'(\d+)\s*([\+\-\*\/x])\s*(\d+)', cleaned)
    if math_pattern or any(word in cleaned for word in ['calculate', 'what is'] if re.search(r'\d', cleaned)):
        return "math", math_pattern

    # Match against intent patterns
    best_match = None
    best_score = 0

    for intent, data in INTENTS.items():
        if intent in ("unknown", "math"):
            continue
        for pattern in data["patterns"]:
            # Check if pattern words appear in input
            pattern_words = pattern.split()
            matches = sum(1 for word in pattern_words if word in cleaned)
            score = matches / len(pattern_words) if pattern_words else 0

            # Boost score for exact phrase match
            if pattern in cleaned:
                score += 0.5

            if score > best_score:
                best_score = score
                best_match = intent

    if best_score >= 0.4:
        return best_match, None

    return "unknown", None


def calculate_math(expression):
    """Safely evaluate a math expression."""
    try:
        math_pattern = re.search(r'(\d+\.?\d*)\s*([\+\-\*\/x])\s*(\d+\.?\d*)', expression)
        if math_pattern:
            a = float(math_pattern.group(1))
            op = math_pattern.group(2)
            b = float(math_pattern.group(3))

            if op == '+':
                result = a + b
                symbol = '+'
            elif op == '-':
                result = a - b
                symbol = '-'
            elif op in ('*', 'x'):
                result = a * b
                symbol = '×'
            elif op == '/':
                if b == 0:
                    return "❌ Cannot divide by zero!"
                result = a / b
                symbol = '÷'

            result = int(result) if result == int(result) else round(result, 4)
            return f"🧮 {a} {symbol} {b} = {result}"
    except Exception:
        pass
    return None


def detect_sentiment(text):
    """Simple sentiment detection."""
    positive = ["good", "great", "awesome", "amazing", "love", "happy",
                "excellent", "perfect", "wonderful", "fantastic"]
    negative = ["bad", "terrible", "hate", "awful", "sad", "angry",
                "horrible", "worst", "disappointed", "upset"]

    cleaned = text.lower()
    pos_count = sum(1 for w in positive if w in cleaned)
    neg_count = sum(1 for w in negative if w in cleaned)

    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    return "neutral"


def get_response(intent, user_input, math_match=None):
    """Get appropriate response for detected intent."""

    if intent == "math":
        result = calculate_math(user_input)
        if result:
            return result
        return "I couldn't calculate that. Try something like '25 + 75' or '100 / 4'! 🧮"

    if intent == "time":
        return f"⏰ Current time: {datetime.now().strftime('%I:%M %p')} ({datetime.now().strftime('%H:%M')})"

    if intent == "date":
        return f"📅 Today is {datetime.now().strftime('%A, %B %d, %Y')}"

    if intent in INTENTS and INTENTS[intent]["responses"]:
        response = random.choice(INTENTS[intent]["responses"])

        # Add sentiment-based prefix
        sentiment = detect_sentiment(user_input)
        if sentiment == "negative" and intent == "unknown":
            response = "I sense some frustration — sorry about that! 😔 " + response

        return response

    return random.choice(INTENTS["unknown"]["responses"])


# ─── CHAT INTERFACE ───────────────────────────────────────────

def print_header():
    clear_screen()
    print("\n" + "=" * 55)
    print("          🤖 SOHAIBBOT — AI CHATBOT")
    print("          Muhammad Sohaib Imran | FAST-NUCES")
    print("          Natural Language Processing")
    print("=" * 55)
    print("\n  Hello! I'm SohaibBot 👋")
    print("  Ask me about crypto, finance, AI, tech & more!")
    print("  Type 'help' for commands | 'quit' to exit\n")
    print("  " + "─" * 50)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def format_bot_response(response):
    """Format bot response with prefix."""
    print(f"\n  🤖 SohaibBot: {response}\n")


def format_user_input(text):
    """Format user input display."""
    return f"  👤 You: {text}"


def main():
    """Main chatbot loop."""
    print_header()

    conversation_count = 0
    history = []

    while True:
        try:
            user_input = input("  👤 You: ").strip()
        except (KeyboardInterrupt, EOFError):
            format_bot_response("Goodbye! It was great chatting with you! 👋")
            break

        if not user_input:
            continue

        # Exit commands
        if user_input.lower() in ['quit', 'exit', 'q']:
            format_bot_response("Goodbye! Have a great day! 👋")
            break

        # Clear screen command
        if user_input.lower() in ['clear', 'cls']:
            print_header()
            continue

        # History command
        if user_input.lower() == 'history':
            if history:
                print("\n  📜 CONVERSATION HISTORY")
                print("  " + "─" * 40)
                for h in history[-10:]:
                    print(f"  👤 {h['user']}")
                    print(f"  🤖 {h['bot'][:60]}...")
                    print()
            else:
                print("\n  No history yet!\n")
            continue

        # Detect intent and generate response
        intent, extra = detect_intent(user_input)
        response = get_response(intent, user_input, extra)

        # Display response
        format_bot_response(response)

        # Save to history
        history.append({"user": user_input, "bot": response})
        conversation_count += 1

        # Every 5 messages, add a friendly nudge
        if conversation_count % 5 == 0:
            print(f"  💬 We've exchanged {conversation_count} messages! Type 'help' to explore more topics.\n")


if __name__ == "__main__":
    main()
