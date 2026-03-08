/**
 * API Client for Todo AI Chatbot
 *
 * Direct API calls to backend with Better Auth cookie support
 */

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export interface Message {
  id: string;
  conversation_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at: string;
}

export interface ToolCall {
  tool: string;
  result: Record<string, any>;
}

export interface ChatResponse {
  conversation_id: string;
  message: Message;
  tool_calls: ToolCall[];
}

export interface Conversation {
  id: string;  // UUID as string for easy comparison
  user_id: string;
  session_id: string;
  created_at: string;
  updated_at: string;
}

/**
 * Debug: Log available cookies
 */
function logCookies(): void {
  console.log('Available cookies:', document.cookie);
  const cookieNames = [
    'better-auth.session_token',
    'better-auth.session-token',
    'session_token',
    'auth_token',
  ];
  cookieNames.forEach(name => {
    const value = document.cookie
      .split('; ')
      .find(row => row.startsWith(name + '='))
      ?.split('=')[1];
    console.log(`Cookie ${name}: ${value ? 'PRESENT' : 'NOT FOUND'}`);
  });
}

/**
 * Handle fetch errors gracefully with detailed logging
 */
async function handleFetch<T>(
  url: string,
  options: RequestInit,
  operationName: string
): Promise<T> {
  console.log(`[${operationName}] Fetching URL: ${url}`);
  console.log(`[${operationName}] Request options:`, JSON.stringify(options, null, 2));

  try {
    const response = await fetch(url, options);
    
    if (!response.ok) {
      let errorData: any;
      try {
        errorData = await response.json();
        console.error(`[${operationName}] HTTP ${response.status}:`, errorData);
      } catch (parseError) {
        errorData = { detail: `HTTP ${response.status}: ${response.statusText}` };
        console.error(`[${operationName}] Failed to parse error response:`, parseError);
      }
      
      // Handle specific error codes
      if (response.status === 402) {
        throw new Error(
          'Insufficient API credits. This request requires more credits or fewer tokens. ' +
          'Please visit https://openrouter.ai/settings/credits to add credits or contact support.'
        );
      }
      
      // Log full error details for AI/chat errors
      if (url.includes('/api/chat/')) {
        console.error(`[${operationName}] === FULL ERROR DATA ===`);
        console.error(`[${operationName}] Status: ${response.status}`);
        console.error(`[${operationName}] Status Text: ${response.statusText}`);
        console.error(`[${operationName}] Response Headers:`, Object.fromEntries(response.headers.entries()));
        console.error(`[${operationName}] Error Data:`, JSON.stringify(errorData, null, 2));
        console.error(`[${operationName}] === END ERROR DATA ===`);
        
        // Check if error contains AI processing failure
        if (errorData.detail && errorData.detail.includes('AI processing failed')) {
          console.error(`[${operationName}] ⚠️ AI PROCESSING ERROR - Check backend terminal for tool call details`);
        }
      }
      
      throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    console.log(`[${operationName}] Success:`, data);
    return data;
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      console.error(`[${operationName}] Connection error - Cannot reach backend at ${url}`);
      console.error(`[${operationName}] Error details:`, error.message);
      console.error(`[${operationName}] Troubleshooting:`);
      console.error(`[${operationName}]   1. Ensure backend server is running on port 8000`);
      console.error(`[${operationName}]   2. Check CORS configuration in main.py`);
      console.error(`[${operationName}]   3. Verify NEXT_PUBLIC_API_BASE_URL environment variable`);
      throw new Error(
        `Cannot connect to backend server at ${url}. ` +
        `Please ensure the backend is running on port 8000 and CORS is properly configured.`
      );
    }
    console.error(`[${operationName}] Request failed:`, error);
    throw error;
  }
}

/**
 * Send a message to the AI chatbot
 */
export async function sendMessage(
  message: string,
  conversationId?: string
): Promise<ChatResponse> {
  const url = `${BASE_URL}/api/chat/`;
  console.log(`[sendMessage] Attempting to connect to: ${url}`);
  logCookies();

  return handleFetch<ChatResponse>(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({
      message,
      conversation_id: conversationId,
    }),
  }, 'sendMessage');
}

/**
 * Create a new conversation
 */
export async function createConversation(): Promise<Conversation> {
  const url = `${BASE_URL}/api/chat/conversations`;
  logCookies();

  return handleFetch<Conversation>(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
  }, 'createConversation');
}

/**
 * Get message history for a conversation
 */
export async function getConversationMessages(
  conversationId: string
): Promise<{ messages: Message[]; count: number }> {
  const url = `${BASE_URL}/api/chat/conversations/${conversationId}/messages`;
  logCookies();

  return handleFetch<{ messages: Message[]; count: number }>(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
  }, 'getConversationMessages');
}

/**
 * List all conversations
 */
export async function listConversations(): Promise<Conversation[]> {
  const url = `${BASE_URL}/api/chat/conversations`;
  console.log(`[listConversations] Attempting to connect to: ${url}`);
  logCookies();

  return handleFetch<Conversation[]>(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
  }, 'listConversations');
}

/**
 * Delete a conversation
 */
export async function deleteConversation(
  conversationId: string
): Promise<{ success: boolean; deleted_conversation_id: string }> {
  const url = `${BASE_URL}/api/chat/conversations/${conversationId}`;
  console.log(`[deleteConversation] Deleting conversation: ${conversationId}`);
  console.log(`[deleteConversation] URL: ${url}`);
  logCookies();

  return handleFetch<{ success: boolean; deleted_conversation_id: string }>(url, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
  }, 'deleteConversation');
}
