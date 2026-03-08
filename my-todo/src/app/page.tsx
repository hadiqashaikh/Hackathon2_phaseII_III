'use client';

/**
 * Unified Dashboard - Todo List + AI Chatbot
 * Modern Dark Theme with Slate/Zinc colors, Glassmorphism effects
 * Split-screen layout with Sidebar navigation
 */

import React, { useState, useEffect, useRef } from 'react';
import { authClient } from '@/lib/auth-client';
import {
  sendMessage,
  createConversation,
  getConversationMessages,
  listConversations,
  deleteConversation,
  Conversation as ConversationType,
} from '@/lib/api';
import {
  Send,
  Bot,
  User,
  Loader2,
  Trash2,
  MessageSquare,
  CheckCircle2,
  Circle,
  Pencil,
  X,
  Menu,
  ChevronLeft,
  ChevronRight,
  Plus,
  Sparkles,
} from 'lucide-react';

// ============================================
// Types
// ============================================

interface Task {
  id: string;
  title: string;
  completed: boolean;
}

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
  tool_calls?: Array<{ tool: string; result: Record<string, any> }>;
}

// ============================================
// Main Component
// ============================================

export default function UnifiedDashboard() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [taskInput, setTaskInput] = useState('');
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');

  // Chat state
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [chatInput, setChatInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [conversations, setConversations] = useState<ConversationType[]>([]);
  const [showSidebar, setShowSidebar] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatInputRef = useRef<HTMLTextAreaElement>(null);

  const { data: session, isPending } = authClient.useSession();

  // Scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load tasks when session is available
  useEffect(() => {
    if (session) {
      fetchTasks();
      loadConversations();
    }
  }, [session]);

  // ============================================
  // Task Functions
  // ============================================

  const fetchTasks = async () => {
    try {
      const res = await fetch('/api/tasks');
      const data = await res.json();
      if (Array.isArray(data)) setTasks(data);
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
    }
  };

  const addTask = async () => {
    if (!taskInput.trim()) return;
    try {
      const res = await fetch('/api/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: taskInput }),
      });
      if (res.ok) {
        const newTask = await res.json();
        setTasks((prev) => [...prev, newTask]);
        setTaskInput('');
      }
    } catch (error) {
      console.error('Failed to add task:', error);
    }
  };

  const toggleComplete = async (task: Task) => {
    try {
      const res = await fetch('/api/tasks', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: task.id, completed: !task.completed }),
      });
      if (res.ok) {
        const updated = await res.json();
        setTasks((prev) => prev.map((t) => (t.id === task.id ? updated : t)));
      }
    } catch (error) {
      console.error('Failed to toggle task:', error);
    }
  };

  const editTask = async (id: string, oldTitle: string) => {
    const newTitle = prompt('Update mission:', oldTitle);
    if (!newTitle || newTitle === oldTitle) return;
    try {
      const res = await fetch('/api/tasks', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, title: newTitle }),
      });
      if (res.ok) {
        const updated = await res.json();
        setTasks((prev) => prev.map((t) => (t.id === id ? updated : t)));
      }
    } catch (error) {
      console.error('Failed to edit task:', error);
    }
  };

  const deleteTask = async (id: string) => {
    try {
      const res = await fetch('/api/tasks', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id }),
      });
      if (res.ok) setTasks((prev) => prev.filter((t) => t.id !== id));
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  };

  // ============================================
  // Chat Functions
  // ============================================

  async function loadConversations() {
    try {
      const list = await listConversations();
      console.log('[loadConversations] Loaded conversations:', list);
      setConversations(list);
    } catch (error) {
      console.error('Failed to load conversations:', error);
    }
  }

  async function startNewConversation() {
    try {
      setIsLoading(true);
      const conv = await createConversation();
      console.log('[startNewConversation] Created conversation:', conv);
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
      console.log('[loadConversation] Loading conversation:', id);
      setIsLoading(true);
      const data = await getConversationMessages(id);
      setConversationId(id);
      setMessages(data.messages.map((m) => ({
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
      console.log('[handleDeleteConversation] Deleting conversation:', id);
      await deleteConversation(id);
      if (id === conversationId) {
        setConversationId(null);
        setMessages([]);
      }
      await loadConversations();
    } catch (error: any) {
      console.error('Failed to delete conversation:', error);
      // Show user-friendly error message
      const errorMessage = error.message || 'Failed to delete conversation';
      if (errorMessage.includes('404')) {
        alert('Conversation not found. It may have already been deleted.');
        // Refresh the list to show current state
        await loadConversations();
      }
    }
  }

  async function handleChatSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!chatInput.trim() || isLoading) return;

    const userMessage = chatInput.trim();
    setChatInput('');

    const newUserMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: userMessage,
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, newUserMessage]);
    setIsLoading(true);

    try {
      const response = await sendMessage(userMessage, conversationId || undefined);

      if (!conversationId) {
        setConversationId(response.conversation_id);
        await loadConversations();
      }

      const aiMessage: ChatMessage = {
        id: response.message.id,
        role: 'assistant',
        content: response.message.content,
        created_at: response.message.created_at,
        tool_calls: response.tool_calls,
      };

      setMessages((prev) => [...prev, aiMessage]);
      
      // 🔄 Refresh tasks if AI used any task-related tools
      if (response.tool_calls && response.tool_calls.length > 0) {
        const taskTools = ['add_task_tool', 'complete_task_tool', 'delete_task_tool', 'update_task_tool', 'list_tasks_tool'];
        const usedTaskTool = response.tool_calls.some(tc => taskTools.includes(tc.tool));
        if (usedTaskTool) {
          console.log('[handleChatSubmit] Task tool detected, refreshing tasks...');
          await fetchTasks();
        }
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      const errorMessage: ChatMessage = {
        id: Date.now().toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      chatInputRef.current?.focus();
    }
  }

  const handleChatKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleChatSubmit(e);
    }
  };

  // ============================================
  // Auth Handlers
  // ============================================

  const handleAuth = async () => {
    try {
      if (isLogin) {
        await authClient.signIn.email({ email, password });
      } else {
        await authClient.signUp.email({ email, password, name });
      }
      window.location.reload();
    } catch (err) {
      alert('Auth failed! Check credentials.');
    }
  };

  // ============================================
  // Loading State
  // ============================================

  if (isPending) {
    return (
      <div className="flex h-screen items-center justify-center bg-slate-950">
        <div className="text-center">
          <Loader2 className="h-12 w-12 animate-spin text-blue-500 mx-auto mb-4" />
          <p className="text-slate-400">Loading Orbit...</p>
        </div>
      </div>
    );
  }

  // ============================================
  // Not Authenticated - Login Screen
  // ============================================

  if (!session) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4 relative overflow-hidden">
        {/* Background gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-950 via-slate-950 to-black" />
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl" />

        <div className="relative z-10 w-full max-w-md">
          <div className="backdrop-blur-xl bg-slate-900/50 border border-slate-700/50 rounded-3xl p-8 shadow-2xl">
            <div className="text-center mb-8">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 mb-4 shadow-lg">
                <Sparkles className="h-8 w-8 text-white" />
              </div>
              <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                {isLogin ? 'Welcome Back' : 'Join Orbit'}
              </h2>
              <p className="text-slate-400 mt-2">
                {isLogin ? 'Sign in to manage your tasks' : 'Create an account to get started'}
              </p>
            </div>

            {!isLogin && (
              <input
                placeholder="Name"
                onChange={(e) => setName(e.target.value)}
                className="w-full px-4 py-3 bg-slate-800/50 border border-slate-600/50 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent transition-all mb-3"
              />
            )}
            <input
              placeholder="Email"
              type="email"
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 bg-slate-800/50 border border-slate-600/50 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent transition-all mb-3"
            />
            <input
              type="password"
              placeholder="Password"
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 bg-slate-800/50 border border-slate-600/50 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent transition-all mb-6"
            />
            <button
              onClick={handleAuth}
              className="w-full py-3.5 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white rounded-xl font-semibold shadow-lg shadow-blue-500/25 transition-all duration-200 transform hover:scale-[1.02]"
            >
              {isLogin ? 'Sign In' : 'Sign Up'}
            </button>
            <p
              onClick={() => setIsLogin(!isLogin)}
              className="text-center text-slate-400 mt-6 cursor-pointer hover:text-slate-300 transition-colors"
            >
              {isLogin ? "Need an account? Sign Up" : "Already have an account? Sign In"}
            </p>
          </div>
        </div>
      </div>
    );
  }

  // ============================================
  // Authenticated - Unified Dashboard
  // ============================================

  return (
    <div className="flex h-screen bg-slate-950 overflow-hidden">
      {/* Sidebar */}
      <div
        className={`fixed inset-y-0 left-0 z-50 w-72 bg-slate-900/80 backdrop-blur-xl border-r border-slate-700/50 transform transition-transform duration-300 ease-in-out lg:relative lg:transform-none lg:w-80 ${
          showSidebar ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        } ${sidebarCollapsed ? 'lg:w-20' : ''}`}
      >
        <div className="flex flex-col h-full">
          {/* Sidebar Header */}
          <div className="p-4 border-b border-slate-700/50 flex items-center justify-between">
            {!sidebarCollapsed && (
              <h2 className="text-lg font-semibold text-white">Conversations</h2>
            )}
            <button
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              className="p-2 hover:bg-slate-800/50 rounded-lg transition-colors hidden lg:block"
            >
              {sidebarCollapsed ? (
                <ChevronRight className="h-5 w-5 text-slate-400" />
              ) : (
                <ChevronLeft className="h-5 w-5 text-slate-400" />
              )}
            </button>
            <button
              onClick={() => setShowSidebar(false)}
              className="lg:hidden p-2 hover:bg-slate-800/50 rounded-lg"
            >
              <X className="h-5 w-5 text-slate-400" />
            </button>
          </div>

          {/* New Chat Button */}
          {!sidebarCollapsed && (
            <div className="p-4">
              <button
                onClick={startNewConversation}
                disabled={isLoading}
                className="w-full px-4 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white rounded-xl transition-all flex items-center justify-center gap-2 disabled:opacity-50 shadow-lg shadow-blue-500/25"
              >
                <Plus className="h-5 w-5" />
                New Chat
              </button>
            </div>
          )}

          {/* Conversation List */}
          <div className="flex-1 overflow-y-auto p-2 space-y-1">
            {conversations.length === 0 ? (
              !sidebarCollapsed && (
                <p className="text-center text-slate-500 py-8 text-sm">
                  No conversations yet
                </p>
              )
            ) : (
              conversations.map((conv) => (
                <div
                  key={conv.id}
                  onClick={() => loadConversation(conv.id)}
                  className={`group flex items-center justify-between p-3 rounded-xl cursor-pointer transition-all ${
                    conv.id === conversationId
                      ? 'bg-blue-500/20 border border-blue-500/30'
                      : 'hover:bg-slate-800/50 border border-transparent'
                  } ${sidebarCollapsed ? 'justify-center' : ''}`}
                >
                  {!sidebarCollapsed ? (
                    <>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-white truncate">
                          Conversation
                        </p>
                        <p className="text-xs text-slate-500">
                          {new Date(conv.created_at).toLocaleDateString()}
                        </p>
                      </div>
                      <button
                        onClick={(e) => handleDeleteConversation(conv.id, e)}
                        className="opacity-0 group-hover:opacity-100 p-2 hover:bg-red-500/20 rounded-lg transition"
                      >
                        <Trash2 className="h-4 w-4 text-red-400" />
                      </button>
                    </>
                  ) : (
                    <MessageSquare className="h-5 w-5 text-slate-400" />
                  )}
                </div>
              ))
            )}
          </div>

          {/* User Info */}
          {!sidebarCollapsed && (
            <div className="p-4 border-t border-slate-700/50">
              <div className="flex items-center gap-3 p-3 rounded-xl bg-slate-800/30">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                  <User className="h-5 w-5 text-white" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-white truncate">
                    {session?.user?.name}
                  </p>
                  <p className="text-xs text-slate-500 truncate">
                    {session?.user?.email}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Overlay for mobile sidebar */}
      {showSidebar && (
        <div
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 lg:hidden"
          onClick={() => setShowSidebar(false)}
        />
      )}

      {/* Main Content - Split Screen */}
      <div className="flex-1 flex flex-col lg:flex-row min-w-0">
        {/* Left Panel - Todo List */}
        <div className="flex-1 flex flex-col min-w-0 border-r border-slate-700/50">
          {/* Header */}
          <div className="p-6 border-b border-slate-700/50">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                  TASK ORBIT
                </h1>
                <p className="text-slate-400 text-sm mt-1">
                  Welcome back, {session?.user?.name}
                </p>
              </div>
              <div className="flex items-center gap-3">
                <button
                  onClick={() => setShowSidebar(true)}
                  className="lg:hidden p-2 hover:bg-slate-800/50 rounded-lg transition-colors"
                >
                  <Menu className="h-5 w-5 text-slate-400" />
                </button>
                <button
                  onClick={async () => {
                    await authClient.signOut();
                    window.location.href = '/';
                  }}
                  className="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 border border-red-500/30 rounded-xl transition-all font-medium"
                >
                  Logout
                </button>
              </div>
            </div>

            {/* Add Task Input */}
            <div className="flex gap-3 items-center backdrop-blur-xl bg-slate-800/30 border border-slate-700/50 rounded-2xl p-2">
              <input
                value={taskInput}
                onChange={(e) => setTaskInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && addTask()}
                placeholder="Launch a new mission..."
                className="flex-1 bg-transparent border-none text-white placeholder-slate-500 px-4 py-2 focus:outline-none"
              />
              <button
                onClick={addTask}
                className="px-6 py-2.5 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white rounded-xl font-semibold transition-all shadow-lg shadow-blue-500/25"
              >
                Add
              </button>
            </div>
          </div>

          {/* Task List */}
          <div className="flex-1 overflow-y-auto p-6">
            <div className="space-y-3">
              {tasks.length === 0 ? (
                <div className="text-center py-12">
                  <Circle className="h-16 w-16 text-slate-700 mx-auto mb-4" />
                  <p className="text-slate-500">No tasks yet. Add one above!</p>
                </div>
              ) : (
                tasks.map((task, index) => (
                  <div
                    key={task.id}
                    className="group flex items-center justify-between p-4 backdrop-blur-xl bg-slate-800/30 border border-slate-700/50 rounded-2xl hover:border-slate-600/50 transition-all duration-200"
                    style={{ animation: `fadeInUp 0.4s ease forwards ${index * 0.05}s` }}
                  >
                    <div className="flex items-center gap-4 flex-1">
                      <button
                        onClick={() => toggleComplete(task)}
                        className={`flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all ${
                          task.completed
                            ? 'bg-green-500 border-green-500'
                            : 'border-slate-500 hover:border-blue-500'
                        }`}
                      >
                        {task.completed && <CheckCircle2 className="h-4 w-4 text-white" />}
                      </button>
                      <span
                        className={`text-base ${
                          task.completed
                            ? 'text-slate-500 line-through'
                            : 'text-white'
                        }`}
                      >
                        {task.title}
                      </span>
                    </div>
                    <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button
                        onClick={() => editTask(task.id, task.title)}
                        className="p-2 hover:bg-blue-500/20 rounded-lg transition-colors"
                      >
                        <Pencil className="h-4 w-4 text-blue-400" />
                      </button>
                      <button
                        onClick={() => deleteTask(task.id)}
                        className="p-2 hover:bg-red-500/20 rounded-lg transition-colors"
                      >
                        <Trash2 className="h-4 w-4 text-red-400" />
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Right Panel - Chat */}
        <div className="flex-1 flex flex-col min-w-0">
          {/* Chat Header */}
          <div className="p-4 border-b border-slate-700/50 flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg">
              <Bot className="h-5 w-5 text-white" />
            </div>
            <div>
              <h2 className="font-semibold text-white">AI Assistant</h2>
              <p className="text-xs text-slate-400">
                {conversationId ? 'Chat active' : 'Start a new conversation'}
              </p>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-center text-slate-500">
                <div className="w-20 h-20 rounded-full bg-gradient-to-br from-blue-500/20 to-purple-600/20 flex items-center justify-center mb-4">
                  <Bot className="h-10 w-10 text-blue-400" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-2">
                  Todo AI Chatbot
                </h3>
                <p className="max-w-md mb-4">
                  I can help you manage your tasks through natural conversation.
                </p>
                <div className="space-y-2 text-sm">
                  <p className="backdrop-blur-xl bg-slate-800/30 px-4 py-2 rounded-full border border-slate-700/50">
                    &quot;Add a task to buy groceries&quot;
                  </p>
                  <p className="backdrop-blur-xl bg-slate-800/30 px-4 py-2 rounded-full border border-slate-700/50">
                    &quot;What tasks do I have?&quot;
                  </p>
                  <p className="backdrop-blur-xl bg-slate-800/30 px-4 py-2 rounded-full border border-slate-700/50">
                    &quot;Mark my first task as complete&quot;
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
          <div className="p-4 border-t border-slate-700/50">
            <form onSubmit={handleChatSubmit} className="flex gap-3">
              <textarea
                ref={chatInputRef}
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyDown={handleChatKeyDown}
                placeholder="Ask me anything..."
                rows={1}
                className="flex-1 resize-none backdrop-blur-xl bg-slate-800/30 border border-slate-700/50 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent"
                style={{ minHeight: '48px', maxHeight: '120px' }}
              />
              <button
                type="submit"
                disabled={!chatInput.trim() || isLoading}
                className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 shadow-lg shadow-blue-500/25"
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

      {/* Global Styles */}
      <style jsx global>{`
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        body {
          background: #020617;
          margin: 0;
        }
        /* Custom scrollbar */
        ::-webkit-scrollbar {
          width: 6px;
          height: 6px;
        }
        ::-webkit-scrollbar-track {
          background: rgba(30, 41, 59, 0.5);
        }
        ::-webkit-scrollbar-thumb {
          background: rgba(71, 85, 105, 0.5);
          border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover {
          background: rgba(100, 116, 139, 0.5);
        }
      `}</style>
    </div>
  );
}

// ============================================
// Message Bubble Component with Glassmorphism
// ============================================

function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === 'user';

  return (
    <div
      className={`flex gap-3 max-w-3xl ${isUser ? 'ml-auto flex-row-reverse' : ''}`}
    >
      {/* Avatar */}
      <div
        className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
          isUser
            ? 'bg-gradient-to-br from-blue-500 to-purple-600'
            : 'bg-slate-700'
        }`}
      >
        {isUser ? (
          <User className="h-4 w-4 text-white" />
        ) : (
          <Bot className="h-4 w-4 text-white" />
        )}
      </div>

      {/* Message Content with Glassmorphism */}
      <div
        className={`px-4 py-3 rounded-2xl max-w-[80%] backdrop-blur-xl border transition-all ${
          isUser
            ? 'bg-gradient-to-br from-blue-600/80 to-purple-600/80 border-blue-400/30 text-white rounded-br-none shadow-lg shadow-blue-500/20'
            : 'bg-slate-800/60 border-slate-600/30 text-white rounded-bl-none'
        }`}
      >
        <p className="whitespace-pre-wrap break-words">{message.content}</p>

        {/* Tool Call Indicators */}
        {message.tool_calls && message.tool_calls.length > 0 && (
          <div className="mt-2 pt-2 border-t border-white/10">
            {message.tool_calls.map((tc, idx) => (
              <ToolCallIndicator key={idx} toolCall={tc} />
            ))}
          </div>
        )}

        {/* Timestamp */}
        <p
          className={`text-xs mt-1 ${
            isUser ? 'text-blue-200' : 'text-slate-400'
          }`}
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

// ============================================
// Tool Call Indicator
// ============================================

function ToolCallIndicator({
  toolCall,
}: {
  toolCall: { tool: string; result: Record<string, any> };
}) {
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
    <div className="flex items-center gap-2 text-sm bg-white/10 px-3 py-1.5 rounded-full text-white/90">
      <span>{getToolMessage()}</span>
    </div>
  );
}

// ============================================
// Typing Indicator
// ============================================

function TypingIndicator() {
  return (
    <div className="flex gap-3 max-w-3xl">
      <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center">
        <Bot className="h-4 w-4 text-white" />
      </div>
      <div className="backdrop-blur-xl bg-slate-800/60 border border-slate-600/30 px-4 py-3 rounded-2xl rounded-bl-none">
        <div className="flex gap-1">
          <span
            className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"
            style={{ animationDelay: '0ms' }}
          />
          <span
            className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"
            style={{ animationDelay: '150ms' }}
          />
          <span
            className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"
            style={{ animationDelay: '300ms' }}
          />
        </div>
      </div>
    </div>
  );
}
