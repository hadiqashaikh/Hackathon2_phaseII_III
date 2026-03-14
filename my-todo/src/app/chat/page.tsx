'use client';

/**
 * Chat Page - Todo AI Chatbot Interface
 * A WhatsApp-style chat UI for managing tasks through natural language
 */

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Send, Bot, User, Loader2, Trash2, MessageSquare, CheckCircle2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { authClient } from '@/lib/auth-client';
import {
  sendMessage,
  createConversation,
  getConversationMessages,
  listConversations,
  deleteConversation,
  Conversation as ConversationType,
  listTasks,
} from '@/lib/api';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
  tool_calls?: Array<{ tool: string; result: Record<string, any> }>;
}

export default function ChatPage() {
  const router = useRouter();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Use Better Auth session hook
  const { data: session, isPending } = authClient.useSession();

  // State
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [conversations, setConversations] = useState<ConversationType[]>([]);
  const [showSidebar, setShowSidebar] = useState(false);
  const [tasks, setTasks] = useState<Array<{ id: string; title: string; completed: boolean }>>([]);

  // Scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load conversations for sidebar when session is available
  useEffect(() => {
    if (session) {
      loadConversations();
      loadTasks();
    }
  }, [session]);

  async function loadConversations() {
    try {
      const list = await listConversations();
      setConversations(list);
    } catch (error) {
      console.error('Failed to load conversations:', error);
    }
  }

  async function loadTasks() {
    try {
      const taskList = await listTasks();
      setTasks(taskList);
      console.log('[loadTasks] Loaded tasks:', taskList);
    } catch (error) {
      console.error('Failed to load tasks:', error);
    }
  }

  async function startNewConversation() {
    try {
      setIsLoading(true);
      const conv = await createConversation();
      setConversationId(conv.id);
      setMessages([]);
      setShowSidebar(false);
      await loadConversations();
    } catch (error) {
      console.error('Failed to create conversation:', error);
    } finally {
      setIsLoading(false);
    }
  }

  async function loadConversation(id: string) {
    try {
      setIsLoading(true);
      const data = await getConversationMessages(id);
      setConversationId(id);
      setMessages(data.messages.map(m => ({
        id: m.id,
        role: m.role as 'user' | 'assistant',
        content: m.content,
        created_at: m.created_at,
      })));
      setShowSidebar(false);
    } catch (error) {
      console.error('Failed to load conversation:', error);
    } finally {
      setIsLoading(false);
    }
  }

  async function handleDeleteConversation(id: string, e: React.MouseEvent) {
    e.stopPropagation();
    if (!confirm('Delete this conversation?')) return;

    try {
      await deleteConversation(id);
      if (id === conversationId) {
        setConversationId(null);
        setMessages([]);
      }
      await loadConversations();
    } catch (error) {
      console.error('Failed to delete conversation:', error);
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');

    // Add user message to UI immediately
    const newUserMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: userMessage,
      created_at: new Date().toISOString(),
    };

    setMessages(prev => [...prev, newUserMessage]);
    setIsLoading(true);

    try {
      const response = await sendMessage(userMessage, conversationId || undefined);

      // Update conversation ID if this is a new conversation
      if (!conversationId) {
        setConversationId(response.conversation_id);
        await loadConversations();
      }

      // Add AI response to UI
      const aiMessage: ChatMessage = {
        id: response.message.id,
        role: 'assistant',
        content: response.message.content,
        created_at: response.message.created_at,
        tool_calls: response.tool_calls,
      };

      setMessages(prev => [...prev, aiMessage]);

      // Refresh tasks if AI made changes (add/delete/update/complete task)
      if (response.tool_calls && response.tool_calls.length > 0) {
        console.log('[handleSubmit] Tool calls detected, refreshing tasks:', response.tool_calls);
        await loadTasks();
      }
    } catch (error) {
      console.error('Failed to send message:', error);

      // Add error message
      const errorMessage: ChatMessage = {
        id: Date.now().toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        created_at: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  }

  // Handle Enter key to send (Shift+Enter for new line)
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Loading state - show spinner while checking session
  if (isPending) {
    return (
      <div className="flex h-screen items-center justify-center bg-gray-50">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Loading chat...</p>
        </div>
      </div>
    );
  }

  // Not authenticated - show login prompt (NO redirect loop)
  if (!session) {
    return (
      <div className="flex h-screen items-center justify-center bg-gray-50">
        <div className="text-center max-w-md px-6">
          <Bot className="h-16 w-16 text-gray-400 mx-auto mb-6" />
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            Please log in to chat
          </h1>
          <p className="text-gray-600 mb-6">
            You need to be logged in to use the AI chatbot. 
            You will be redirected back here after login.
          </p>
          <button
            onClick={() => window.location.href = '/'}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium"
          >
            Go to Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar - Conversation List */}
      <div
        className={cn(
          'fixed inset-y-0 left-0 z-50 w-72 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:relative lg:transform-none lg:w-80',
          showSidebar ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        )}
      >
        <div className="flex flex-col h-full">
          {/* Sidebar Header */}
          <div className="p-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-900">
                Conversations
              </h2>
              <button
                onClick={() => setShowSidebar(false)}
                className="lg:hidden p-2 hover:bg-gray-100 rounded-lg"
              >
                <Send className="h-5 w-5 rotate-45" />
              </button>
            </div>
            <button
              onClick={startNewConversation}
              disabled={isLoading}
              className="mt-3 w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition flex items-center justify-center gap-2 disabled:opacity-50"
            >
              <MessageSquare className="h-4 w-4" />
              New Chat
            </button>
          </div>

          {/* Conversation List */}
          <div className="flex-1 overflow-y-auto p-2">
            {conversations.length === 0 ? (
              <p className="text-center text-gray-500 py-8">
                No conversations yet
              </p>
            ) : (
              <div className="space-y-1">
                {conversations.map(conv => (
                  <div
                    key={conv.id}
                    onClick={() => loadConversation(conv.id)}
                    className={cn(
                      'group flex items-center justify-between p-3 rounded-lg cursor-pointer hover:bg-gray-100 transition',
                      conv.id === conversationId && 'bg-blue-50'
                    )}
                  >
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        Conversation
                      </p>
                      <p className="text-xs text-gray-500">
                        {new Date(conv.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <button
                      onClick={(e) => handleDeleteConversation(conv.id, e)}
                      className="opacity-0 group-hover:opacity-100 p-2 hover:bg-red-100 rounded-lg transition"
                    >
                      <Trash2 className="h-4 w-4 text-red-600" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Overlay for mobile sidebar */}
      {showSidebar && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setShowSidebar(false)}
        />
      )}

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Chat Header */}
        <div className="bg-white border-b border-gray-200 px-4 py-3 flex items-center gap-3">
          <button
            onClick={() => setShowSidebar(true)}
            className="lg:hidden p-2 hover:bg-gray-100 rounded-lg"
          >
            <MessageSquare className="h-5 w-5" />
          </button>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
              <Bot className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="font-semibold text-gray-900">Todo AI Assistant</h1>
              <p className="text-sm text-gray-500">
                {conversationId ? 'Chat active' : 'Start a new chat'}
              </p>
            </div>
          </div>
        </div>

        {/* Tasks Panel - Show current tasks */}
        {tasks.length > 0 && (
          <div className="bg-blue-50 border-b border-blue-100 px-4 py-2">
            <div className="flex items-center gap-2 mb-2">
              <CheckCircle2 className="h-4 w-4 text-blue-600" />
              <h3 className="text-sm font-semibold text-blue-900">
                My Tasks ({tasks.length})
              </h3>
            </div>
            <div className="flex flex-wrap gap-2">
              {tasks.slice(0, 5).map(task => (
                <span
                  key={task.id}
                  className={`text-xs px-3 py-1 rounded-full ${
                    task.completed
                      ? 'bg-green-100 text-green-700 line-through'
                      : 'bg-white text-gray-700 border border-gray-200'
                  }`}
                >
                  {task.title}
                </span>
              ))}
              {tasks.length > 5 && (
                <span className="text-xs text-gray-500">
                  +{tasks.length - 5} more
                </span>
              )}
            </div>
          </div>
        )}

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center text-gray-500">
              <Bot className="h-16 w-16 mb-4 text-gray-300" />
              <h2 className="text-xl font-semibold mb-2">
                Welcome to Todo AI Chatbot
              </h2>
              <p className="max-w-md">
                I can help you manage your tasks through natural conversation.
                Try saying:
              </p>
              <div className="mt-4 space-y-2 text-sm">
                <p className="bg-gray-100 px-4 py-2 rounded-full">
                  "Add a task to buy groceries"
                </p>
                <p className="bg-gray-100 px-4 py-2 rounded-full">
                  "What tasks do I have?"
                </p>
                <p className="bg-gray-100 px-4 py-2 rounded-full">
                  "Mark my first task as complete"
                </p>
              </div>
            </div>
          ) : (
            <>
              {messages.map((msg) => (
                <MessageBubble key={msg.id} message={msg} />
              ))}
              {isLoading && messages[messages.length - 1]?.role === 'user' && (
                <TypingIndicator />
              )}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        {/* Input Area */}
        <div className="bg-white border-t border-gray-200 p-4">
          <form onSubmit={handleSubmit} className="flex gap-3 max-w-4xl mx-auto">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type a message..."
              rows={1}
              className="flex-1 resize-none border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              style={{ minHeight: '48px', maxHeight: '120px' }}
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {isLoading ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <Send className="h-5 w-5" />
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

/**
 * Message Bubble Component
 */
function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === 'user';

  return (
    <div
      className={cn(
        'flex gap-3 max-w-3xl',
        isUser ? 'ml-auto flex-row-reverse' : ''
      )}
    >
      {/* Avatar */}
      <div
        className={cn(
          'w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0',
          isUser ? 'bg-gray-300' : 'bg-blue-600'
        )}
      >
        {isUser ? (
          <User className="h-5 w-5 text-gray-600" />
        ) : (
          <Bot className="h-5 w-5 text-white" />
        )}
      </div>

      {/* Message Content */}
      <div
        className={cn(
          'px-4 py-3 rounded-2xl max-w-[80%]',
          isUser
            ? 'bg-blue-600 text-white rounded-br-none'
            : 'bg-gray-100 text-gray-900 rounded-bl-none'
        )}
      >
        <p className="whitespace-pre-wrap break-words">{message.content}</p>
        
        {/* Tool Call Indicators */}
        {message.tool_calls && message.tool_calls.length > 0 && (
          <div className="mt-2 pt-2 border-t border-gray-200/50">
            {message.tool_calls.map((tc, idx) => (
              <ToolCallIndicator key={idx} toolCall={tc} />
            ))}
          </div>
        )}

        {/* Timestamp */}
        <p
          className={cn(
            'text-xs mt-1',
            isUser ? 'text-blue-100' : 'text-gray-500'
          )}
        >
          {new Date(message.created_at).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </p>
      </div>
    </div>
  );
}

/**
 * Tool Call Indicator - Shows what action the AI took
 */
function ToolCallIndicator({ toolCall }: { toolCall: { tool: string; result: Record<string, any> } }) {
  const getToolMessage = () => {
    switch (toolCall.tool) {
      case 'add_task_tool':
        return `✅ Task created: "${toolCall.result.title || 'New task'}"`;
      case 'complete_task_tool':
        return `✓ Task completed`;
      case 'delete_task_tool':
        return `🗑️ Task deleted`;
      case 'update_task_tool':
        return `✏️ Task updated`;
      case 'list_tasks_tool':
        return `📋 Tasks listed`;
      default:
        return `🔧 ${toolCall.tool}`;
    }
  };

  return (
    <div className="flex items-center gap-2 text-sm bg-white/50 px-3 py-1.5 rounded-full">
      <span>{getToolMessage()}</span>
    </div>
  );
}

/**
 * Typing Indicator
 */
function TypingIndicator() {
  return (
    <div className="flex gap-3 max-w-3xl">
      <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
        <Bot className="h-5 w-5 text-white" />
      </div>
      <div className="bg-gray-100 px-4 py-3 rounded-2xl rounded-bl-none">
        <div className="flex gap-1">
          <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
          <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
          <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
        </div>
      </div>
    </div>
  );
}
