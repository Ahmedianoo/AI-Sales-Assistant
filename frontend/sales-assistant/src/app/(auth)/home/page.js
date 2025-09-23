"use client"

import { useState, useEffect, useRef } from "react"
import { Menu, Send, Plus, UserIcon, BotIcon } from "lucide-react"
import styles from './home.module.css'
import { fetchSearchHistory, saveSearchQuery } from "@/app/actions/searchHistory"
import { call_to_chatbot } from "@/app/actions/chatbot"

export default function Home() {
  const [messages, setMessages] = useState([])
  const [inputValue, setInputValue] = useState("")
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [chatHistory, setChatHistory] = useState([])
  const [currentChatId, setCurrentChatId] = useState(null)
  const [currentChatSaved, setCurrentChatSaved] = useState(false)
  const [isLoading, setIsLoading] = useState(false) // Added loading state
  const messagesEndRef = useRef(null)
  const textareaRef = useRef(null)

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const data = await fetchSearchHistory()
        setChatHistory(data)
      } catch (err) {
        console.error("Error loading search history:", err)
      }
    }
    loadHistory()
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"
      const scrollHeight = textareaRef.current.scrollHeight
      textareaRef.current.style.height = Math.min(scrollHeight, 120) + "px"
    }
  }, [inputValue])

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return

    const newMessage = {
      id: Date.now(),
      text: inputValue,
      isUser: true,
      timestamp: new Date(),
    }

    let backendData = null
    if (!currentChatSaved) {
      try {
        backendData = await saveSearchQuery(inputValue)
      } catch (err) {
        console.error("Error saving search query:", err)
      }
    }

    if (messages.length === 0 && !currentChatSaved) {
      const newChat = {
        id: backendData ? backendData.search_id : Date.now(),
        title: inputValue.slice(0, 50) + (inputValue.length > 50 ? "..." : ""),
        messages: [],
      }
      setChatHistory((prev) => [newChat, ...prev])
      setCurrentChatId(newChat.id)
      setCurrentChatSaved(true)
    }

    setMessages((prev) => [...prev, newMessage])
    setInputValue("")
    setIsLoading(true) // start loading for AI response

    try {
      // Call the separate function to post the message and get the AI's response
      console.log("Sending message to backend: ", newMessage.text)
      const aiResponseText = await call_to_chatbot(newMessage.text);

      // Add the AI's response to the chat
      const newAIResponse = {
        id: Date.now() + 1,
        text: aiResponseText,
        isUser: false,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, newAIResponse]);
    } catch (error) {
      // Handle the error from the postMessage function
      const errorResponse = {
        id: Date.now() + 1,
        text: error.message,
        isUser: false,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorResponse]);
    } finally {
      setIsLoading(false);
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const handleChatSelect = (chat) => {
    const sortedMessages = [...chat.messages].sort(
      (a, b) => new Date(a.timestamp) - new Date(b.timestamp)
    )
    setMessages(sortedMessages)
    setCurrentChatId(chat.id)
    setCurrentChatSaved(true)
  }

  const handleNewChat = () => {
    setMessages([])
    setCurrentChatId(null)
    setCurrentChatSaved(false)
  }

  const formatTime = (timestamp) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
  }

  return (
    <div className="h-[calc(100vh-3.25rem)] font-sans" style={{ fontFamily: "var(--font-family-sans)" }}>
      <div className="flex h-full bg-white">

        {/* Sidebar */}
        {sidebarOpen && (
          <div className="w-64 flex flex-col z-50"
            style={{
              backgroundColor: "var(--color-sidebar-custom)",
              borderTop: "1px solid black",
              borderRight: "1px solid black",
            }}>
            <div className="p-4 pt-10 border-gray-200">
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  handleNewChat()
                }}
                className={styles.btn}
              >
                <Plus size={16} />
                New Chat
              </button>
            </div>

          <div className="flex-1 overflow-y-auto p-4">
            <h2 className="font-semibold mb-4">Chat History</h2>
            <div className="space-y-2">
              {chatHistory.map((chat) => (
                <button
                  key={chat.id}
                  onClick={(e) => {
                    e.stopPropagation()
                    handleChatSelect(chat)
                  }}
                  className={`${styles.chatBtn} ${currentChatId === chat.id ? styles.chatBtnActive : ""}`}
                >
                  <div className="text-sm font-medium break-words">{chat.title}</div>
                </button>
              ))}
            </div>
          </div>
        </div>
        )}

        {/* Main Chat Area */}
        <div className="flex-1 flex flex-col">
          {/* Header */}
          <div className="p-4 pt-6 border-b border-gray-200 flex items-center justify-center relative">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="absolute left-4 p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <Menu size={20} />
            </button>
            <h1 className="text-xl font-semibold"
              style={{ color: "var(--secondary-color)" }}>
              Competitor Chat Assistant
            </h1>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4" style={{ height: "calc(100vh - 140px)" }}>
            {messages.length === 0 ? (
              <div className="text-center text-gray-500 mt-20">
                <h2 className="text-2xl font-semibold mb-2" style={{ fontFamily: "var(--font-family-serif)" }}>Welcome to Competitor Chat Assistant</h2>
                <p>Start a conversation to get insights about your competitors and market analysis.</p>
              </div>
            ) : (
              <>
                {messages.map((message) => (
                  <div key={message.id} className={`flex ${message.isUser ? "justify-end" : "justify-start"} items-start gap-2`}>
                    
                    {/* Bot Avatar on left */}
                    {!message.isUser && (
                      <div className="flex-shrink-0">
                        <BotIcon size={24} />
                      </div>
                    )}

                    {/* Message bubble */}
                    <div
                      className="px-4 py-3 rounded-lg break-words"
                      style={{
                        maxWidth: "45rem",
                        backgroundColor: message.isUser
                          ? "var(--color-chat-user)"
                          : "var(--color-chat-ai)",
                        color: message.isUser
                          ? "var(--color-chat-user-foreground)"
                          : "var(--color-chat-ai-foreground)",
                      }}
                    >
                      <div className="whitespace-pre-wrap break-words">{message.text}</div>
                      <div className="text-xs mt-1 text-right opacity-70">{formatTime(message.timestamp)}</div>
                    </div>

                    {/* User Avatar on right */}
                    {message.isUser && (
                      <div className="flex-shrink-0">
                        <UserIcon size={24} />
                      </div>
                    )}
                  </div>
                ))}

                {/* Loading indicator */}
                {isLoading && (
                  <div className="flex items-start gap-2">
                    <div className="flex-shrink-0">
                      <BotIcon size={24} />
                    </div>
                    <div className="bg-gray-200 rounded-lg px-4 py-3 flex gap-1">
                      <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" />
                      <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: "0.1s" }} />
                      <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }} />
                    </div>
                  </div>
                )}
              </>
            )}
            <div ref={messagesEndRef} />
          </div>


          {/* Input */}
          <div className="p-4 border-t border-gray-200 flex-shrink-0">
            <div className="flex justify-center">
              <div className="flex gap-3 items-center w-full max-w-2xl">
                <div className="flex-1 relative">
                  <textarea
                    ref={textareaRef}
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Type your message..."
                    className="w-full p-3 border rounded-lg focus:outline-none resize-none break-words min-h-[48px] max-h-[120px] overflow-y-auto"
                    style={{ backgroundColor: "white", color: "black", verticalAlign: "middle" }}
                    rows={1}
                  />
                </div>
                <button
                  onClick={handleSendMessage}
                  disabled={!inputValue.trim() || isLoading}
                  className="p-3 rounded-lg flex-shrink-0 transition-all duration-150 ease-in-out hover:scale-105 hover:brightness-90 disabled:opacity-50 disabled:cursor-not-allowed"
                  style={{ backgroundColor: "var(--color-accent-color)", color: "white" }}
                >
                  <Send size={20} />
                </button>
              </div>
            </div>
            {/* Shift+Enter note */}
            <div className="text-xs text-gray-500 text-center mt-1">
              Press Enter to send, Shift+Enter for new line
            </div>
          </div>

        </div>
      </div>
    </div>
  )
}
