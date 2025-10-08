// "use client"

// import { useState, useEffect, useRef } from "react"
// import { Menu, Send, Plus, UserIcon, BotIcon } from "lucide-react"
// import styles from './home.module.css'
// import { fetchConversations, fetchChatMessages} from "@/app/actions/searchHistory"
// import { call_to_chatbot } from "@/app/actions/chatbot"

// export default function Home() {
//   const [messages, setMessages] = useState([])
//   const [inputValue, setInputValue] = useState("")
//   const [sidebarOpen, setSidebarOpen] = useState(true)
//   const [chatHistory, setChatHistory] = useState([])
//   const [currentChatId, setCurrentChatId] = useState(null) 
//   const [isLoading, setIsLoading] = useState(false)
//   const messagesEndRef = useRef(null)
//   const textareaRef = useRef(null)

//   // Function to initialize a new conversation thread with a UUID
//   const startNewThread = () => {
    
//     // Prevent creating a thread if one already exists
//     if (currentChatId !== null) return;

//     const newThreadId = crypto.randomUUID()
//     setMessages([])
//     setCurrentChatId(newThreadId)
//   }

//   // Effect 1: Load history for sidebar and initialize a new thread if none exists
//   useEffect(() => {
//     const loadHistory = async () => {
//       try {
//         const data = await fetchConversations()
//         setChatHistory(data) // data.{id, title}
        
//         // // If history is empty and no current chat is active, start a new thread
//         // if (data.length === 0 && currentChatId === null) {
//         //   startNewThread()
//         // }
//       } catch (err) {      
//         // Fallback: If history fails to load, ensure a new thread starts
//         if (currentChatId === null) {
//           //  startNewThread()
//           console.log("no chat id")
//         }
//       }
//     }
//     loadHistory()
//   }, []) // Dependency array ensures this runs once on mount

//   //Effect 2: autoscroll of messages in main chat panel
//   useEffect(() => {
//     messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
//   }, [messages])

//   //Effect 3: expand input text area for larger queries
//   useEffect(() => {
//     if (textareaRef.current) {
//       textareaRef.current.style.height = "auto"
//       const scrollHeight = textareaRef.current.scrollHeight
//       textareaRef.current.style.height = Math.min(scrollHeight, 120) + "px"
//     }
//   }, [inputValue])

//   //Effect 4: 
//   const handleSendMessage = async () => {
//     // Check 1: Message content and loading state
//     if (!inputValue.trim() || isLoading) return;

//     // Check 2: Thread ID MUST be set. If not, set it NOW and use the new ID immediately.
//     let threadIdToSend = currentChatId;
//     if (currentChatId === null) {
//         threadIdToSend = crypto.randomUUID();
//         setCurrentChatId(threadIdToSend); 
//     }
    
//     const newMessage = {
//       id: Date.now(),
//       text: inputValue,
//       isUser: true,
//       timestamp: new Date(),
//     }

//     if (messages.length === 0) {
//       const newChat = {
//         id: threadIdToSend, 
//         title: inputValue.slice(0, 50) + (inputValue.length > 50 ? "..." : ""),
//       }
//       setChatHistory((prev) => [newChat, ...prev])
//     }

//     setMessages((prev) => [...prev, newMessage])
//     setInputValue("")
//     setIsLoading(true) // start loading for AI response

//     try {
//       // Pass the thread ID to the backend for LangGraph persistence
//       console.log(`Sending message to backend for thread ID ${threadIdToSend}: ${newMessage.text}`)
//       const aiResponseText = await call_to_chatbot({query: newMessage.text, thread_id:threadIdToSend});

//       // Add the AI's response to the chat
//       const newAIResponse = {
//         id: Date.now() + 1,
//         text: aiResponseText,
//         isUser: false,
//         timestamp: new Date(),
//       };
//       setMessages((prev) => [...prev, newAIResponse]);
//     } catch (error) {
//       // Handle the error from the postMessage function
//       const errorResponse = {
//         id: Date.now() + 1,
//         text: error.message,
//         isUser: false,
//         timestamp: new Date(),
//       };
//       setMessages((prev) => [...prev, errorResponse]);
//     } finally {
//       setIsLoading(false);
//     }
//   }

//   const handleKeyDown = (e) => {
//     if (e.key === "Enter" && !e.shiftKey) {
//       e.preventDefault()
//       handleSendMessage()
//     }
//   }

//   const handleChatSelect = async(chat) => {
//     setCurrentChatId(chat.id) // This is now the thread_id for persistence
//     //load messages from backend (pass thread_id to backend)
//     const loadedMessages = await fetchChatMessages(chat.id);
//     setMessages(loadedMessages);
//   }

//   const formatTime = (timestamp) => {
//     const date = new Date(timestamp)
//     return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
//   }

//   return (
//     <div className="h-[calc(100vh-3.25rem)] font-sans" style={{ fontFamily: "var(--font-family-sans)" }}>
//       <div className="flex h-full bg-white">

//         {/* Sidebar */}
//         {sidebarOpen && (
//           <div className="w-64 flex flex-col z-50"
//             style={{
//               backgroundColor: "var(--color-sidebar-custom)",
//               borderTop: "1px solid black",
//               borderRight: "1px solid black",
//             }}>
//             <div className="p-4 pt-10 border-gray-200">
//               <button
//                 onClick={(e) => {
//                   e.stopPropagation()
//                   setCurrentChatId(null)
//                   startNewThread() //starts a new thread
//                 }}
//                 className={styles.btn}
//               >
//                 <Plus size={16} />
//                 New Chat
//               </button>
//             </div>

//           <div className="flex-1 overflow-y-auto p-4">
//             <h2 className="font-semibold mb-4">Chat History</h2>
//             <div className="space-y-2">
//               {chatHistory.map((chat) => (
//                 <button
//                   key={chat.id}
//                   onClick={(e) => {
//                     e.stopPropagation()
//                     handleChatSelect(chat)
//                   }}
//                   className={`${styles.chatBtn} ${currentChatId === chat.id ? styles.chatBtnActive : ""}`}
//                 >
//                   <div className="text-sm font-medium break-words">{chat.title}</div>
//                 </button>
//               ))}
//             </div>
//           </div>
//         </div>
//         )}

//         {/* Main Chat Area */}
//         <div className="flex-1 flex flex-col">
//           {/* Header */}
//           <div className="p-4 pt-6 border-b border-gray-200 flex items-center justify-center relative">
//             <button
//               onClick={() => setSidebarOpen(!sidebarOpen)}
//               className="absolute left-4 p-2 hover:bg-gray-100 rounded-lg transition-colors"
//             >
//               <Menu size={20} />
//             </button>
//             <h1 className="text-xl font-semibold"
//               style={{ color: "var(--secondary-color)" }}>
//               Competitor Chat Assistant
//             </h1>
//           </div>

//           {/* Messages */}
//           <div className="flex-1 overflow-y-auto p-4 space-y-4" style={{ height: "calc(100vh - 140px)" }}>
//             {messages.length === 0 ? (
//               <div className="text-center text-gray-500 mt-20">
//                 <h2 className="text-2xl font-semibold mb-2" style={{ fontFamily: "var(--font-family-serif)" }}>Welcome to Competitor Chat Assistant</h2>
//                 <p>Start a conversation to get insights about your competitors and market analysis.</p>
//               </div>
//             ) : (
//               <>
//                 {messages.map((message) => (
//                   <div key={message.id} className={`flex ${message.isUser ? "justify-end" : "justify-start"} items-start gap-2`}>
                    
//                     {/* Bot Avatar on left */}
//                     {!message.isUser && (
//                       <div className="flex-shrink-0">
//                         <BotIcon size={24} />
//                       </div>
//                     )}

//                     {/* Message bubble */}
//                     <div
//                       className="px-4 py-3 rounded-lg break-words"
//                       style={{
//                         maxWidth: "45rem",
//                         backgroundColor: message.isUser
//                           ? "var(--color-chat-user)"
//                           : "var(--color-chat-ai)",
//                         color: message.isUser
//                           ? "var(--color-chat-user-foreground)"
//                           : "var(--color-chat-ai-foreground)",
//                       }}
//                     >
//                       <div className="whitespace-pre-wrap break-words">{message.text}</div>
//                       <div className="text-xs mt-1 text-right opacity-70">{formatTime(message.timestamp)}</div>
//                     </div>

//                     {/* User Avatar on right */}
//                     {message.isUser && (
//                       <div className="flex-shrink-0">
//                         <UserIcon size={24} />
//                       </div>
//                     )}
//                   </div>
//                 ))}

//                 {/* Loading indicator */}
//                 {isLoading && (
//                   <div className="flex items-start gap-2">
//                     <div className="flex-shrink-0">
//                       <BotIcon size={24} />
//                     </div>
//                     <div className="bg-gray-200 rounded-lg px-4 py-3 flex gap-1">
//                       <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" />
//                       <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: "0.1s" }} />
//                       <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }} />
//                     </div>
//                   </div>
//                 )}
//               </>
//             )}
//             <div ref={messagesEndRef} />
//           </div>


//           {/* Input */}
//           <div className="p-4 border-t border-gray-200 flex-shrink-0">
//             <div className="flex justify-center">
//               <div className="flex gap-3 items-center w-full max-w-2xl">
//                 <div className="flex-1 relative">
//                   <textarea
//                     ref={textareaRef}
//                     value={inputValue}
//                     onChange={(e) => setInputValue(e.target.value)}
//                     onKeyDown={handleKeyDown}
//                     placeholder="Type your message..."
//                     className="w-full p-3 border rounded-lg focus:outline-none resize-none break-words min-h-[48px] max-h-[120px] overflow-y-auto"
//                     style={{ backgroundColor: "white", color: "black", verticalAlign: "middle" }}
//                     rows={1}
//                   />
//                 </div>
//                 <button
//                   onClick={handleSendMessage}
//                   disabled={!inputValue.trim() || isLoading}
//                   className="p-3 rounded-lg flex-shrink-0 transition-all duration-150 ease-in-out hover:scale-105 hover:brightness-90 disabled:opacity-50 disabled:cursor-not-allowed"
//                   style={{ backgroundColor: "var(--color-accent-color)", color: "white" }}
//                 >
//                   <Send size={20} />
//                 </button>
//               </div>
//             </div>
//             {/* Shift+Enter note */}
//             <div className="text-xs text-gray-500 text-center mt-1">
//               Press Enter to send, Shift+Enter for new line
//             </div>
//           </div>

//         </div>
//       </div>
//     </div>
//   )
// }

"use client"

import { useState, useEffect, useRef } from "react"
import { Menu, Send, Plus, UserIcon, BotIcon } from "lucide-react"
import styles from './home.module.css'
import { fetchConversations, fetchChatMessages } from "@/app/actions/searchHistory"
import { call_to_chatbot } from "@/app/actions/chatbot"

export default function Home() {
  const [messages, setMessages] = useState([])
  const [inputValue, setInputValue] = useState("")
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [chatHistory, setChatHistory] = useState([])
  const [currentChatId, setCurrentChatId] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)
  const textareaRef = useRef(null)

  // Function to initialize a new conversation thread with a UUID
  const startNewThread = () => {
    const newThreadId = crypto.randomUUID()
    setMessages([])
    setCurrentChatId(newThreadId)

    // Prevent duplicate IDs in chatHistory
    setChatHistory((prev) => {
      if (prev.some((chat) => chat.id === newThreadId)) return prev
      return [{ id: newThreadId, title: "New Chat" }, ...prev]
    })
  }

  // Load history on mount
  useEffect(() => {
    const loadHistory = async () => {
      try {
        const data = await fetchConversations()
        // Ensure no duplicate IDs in data from backend
        const unique = Array.from(new Map(data.map((c) => [c.id, c])).values())
        setChatHistory(unique)
      } catch (err) {
        console.error("Failed to load chat history:", err)
      }
    }
    loadHistory()
  }, [])

  // Autoscroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  // Expand textarea dynamically
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"
      const scrollHeight = textareaRef.current.scrollHeight
      textareaRef.current.style.height = Math.min(scrollHeight, 120) + "px"
    }
  }, [inputValue])

  // Handle sending a message
  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return

    let threadIdToSend = currentChatId
    if (currentChatId === null) {
      threadIdToSend = crypto.randomUUID()
      setCurrentChatId(threadIdToSend)
    }

    const newMessage = {
      id: Date.now(),
      text: inputValue,
      isUser: true,
      timestamp: new Date(),
    }

    // Add chat to sidebar only if it doesn’t already exist
    setChatHistory((prev) => {
      if (!prev.some((chat) => chat.id === threadIdToSend)) {
        const newChat = {
          id: threadIdToSend,
          title: inputValue.slice(0, 50) + (inputValue.length > 50 ? "..." : ""),
        }
        return [newChat, ...prev]
      }
      return prev
    })

    setMessages((prev) => [...prev, newMessage])
    setInputValue("")
    setIsLoading(true)

    try {
      const aiResponseText = await call_to_chatbot({
        query: newMessage.text,
        thread_id: currentChatId,
      })

      const newAIResponse = {
        id: Date.now() + 1,
        text: aiResponseText,
        isUser: false,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, newAIResponse])
    } catch (error) {
      const errorResponse = {
        id: Date.now() + 1,
        text: error.message || "Error sending message.",
        isUser: false,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorResponse])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const handleChatSelect = async (chat) => {
    setCurrentChatId(chat.id)
    try {
      const loadedMessages = await fetchChatMessages(chat.id)
      setMessages(loadedMessages)
    } catch (err) {
      console.error("Failed to load chat messages:", err)
    }
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
          <div
            className="w-64 flex flex-col z-50"
            style={{
              backgroundColor: "var(--color-sidebar-custom)",
              borderTop: "1px solid black",
              borderRight: "1px solid black",
            }}
          >
            <div className="p-4 pt-10 border-gray-200">
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  setCurrentChatId(null)
                  startNewThread()
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
            <h1 className="text-xl font-semibold" style={{ color: "var(--secondary-color)" }}>
              Competitor Chat Assistant
            </h1>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4" style={{ height: "calc(100vh - 140px)" }}>
            {messages.length === 0 ? (
              <div className="text-center text-gray-500 mt-20">
                <h2 className="text-2xl font-semibold mb-2" style={{ fontFamily: "var(--font-family-serif)" }}>
                  Welcome to Competitor Chat Assistant
                </h2>
                <p>Start a conversation to get insights about your competitors and market analysis.</p>
              </div>
            ) : (
              <>
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.isUser ? "justify-end" : "justify-start"} items-start gap-2`}
                  >
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
                      <span
                        className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"
                        style={{ animationDelay: "0.1s" }}
                      />
                      <span
                        className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"
                        style={{ animationDelay: "0.2s" }}
                      />
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
            <div className="text-xs text-gray-500 text-center mt-1">
              Press Enter to send, Shift+Enter for new line
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
