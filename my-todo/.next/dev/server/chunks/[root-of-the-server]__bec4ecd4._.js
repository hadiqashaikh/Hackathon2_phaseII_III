module.exports = [
"[externals]/next/dist/compiled/next-server/app-route-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-route-turbo.runtime.dev.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/compiled/next-server/app-route-turbo.runtime.dev.js", () => require("next/dist/compiled/next-server/app-route-turbo.runtime.dev.js"));

module.exports = mod;
}),
"[externals]/next/dist/compiled/@opentelemetry/api [external] (next/dist/compiled/@opentelemetry/api, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/compiled/@opentelemetry/api", () => require("next/dist/compiled/@opentelemetry/api"));

module.exports = mod;
}),
"[externals]/next/dist/compiled/next-server/app-page-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-page-turbo.runtime.dev.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js", () => require("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/work-unit-async-storage.external.js [external] (next/dist/server/app-render/work-unit-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/server/app-render/work-unit-async-storage.external.js", () => require("next/dist/server/app-render/work-unit-async-storage.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/work-async-storage.external.js [external] (next/dist/server/app-render/work-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/server/app-render/work-async-storage.external.js", () => require("next/dist/server/app-render/work-async-storage.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/shared/lib/no-fallback-error.external.js [external] (next/dist/shared/lib/no-fallback-error.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/shared/lib/no-fallback-error.external.js", () => require("next/dist/shared/lib/no-fallback-error.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/after-task-async-storage.external.js [external] (next/dist/server/app-render/after-task-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/server/app-render/after-task-async-storage.external.js", () => require("next/dist/server/app-render/after-task-async-storage.external.js"));

module.exports = mod;
}),
"[project]/src/app/api/chat/[[...path]]/route.ts [app-route] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "DELETE",
    ()=>DELETE,
    "GET",
    ()=>GET,
    "POST",
    ()=>POST
]);
/**
 * Proxy route for chat API requests to backend
 * This allows cookies from Better Auth to be automatically forwarded
 * 
 * Routes:
 * - POST /api/chat/ - Send message (note the trailing slash)
 * - GET /api/chat/conversations - List conversations
 * - POST /api/chat/conversations - Create conversation
 * - GET /api/chat/conversations/[id]/messages - Get messages
 * - DELETE /api/chat/conversations/[id] - Delete conversation
 */ var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$server$2e$js__$5b$app$2d$route$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/server.js [app-route] (ecmascript)");
;
const BACKEND_URL = ("TURBOPACK compile-time value", "http://localhost:8000") || 'http://localhost:8000';
/**
 * Forward request to backend and preserve authentication cookies
 */ async function proxyRequest(request, method, backendPath, body) {
    try {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
                // Forward the cookie from the incoming request
                Cookie: request.headers.get('cookie') || ''
            },
            credentials: 'include'
        };
        if (body) {
            options.body = JSON.stringify(body);
        }
        const url = `${BACKEND_URL}${backendPath}`;
        console.log(`[Proxy] ${method} ${url}`);
        console.log(`[Proxy] Cookies present: ${!!options.headers.Cookie}`);
        let response;
        try {
            response = await fetch(url, options);
        } catch (fetchError) {
            console.error('[Proxy] Fetch failed:', fetchError.message);
            return __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$server$2e$js__$5b$app$2d$route$5d$__$28$ecmascript$29$__["NextResponse"].json({
                detail: `Backend unavailable: ${fetchError.message}. Make sure the backend is running on ${BACKEND_URL}`
            }, {
                status: 503
            });
        }
        console.log(`[Proxy] Response status: ${response.status}`);
        if (!response.ok) {
            const errorText = await response.text();
            console.error('[Proxy] Backend error:', errorText);
            try {
                const error = JSON.parse(errorText);
                return __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$server$2e$js__$5b$app$2d$route$5d$__$28$ecmascript$29$__["NextResponse"].json(error, {
                    status: response.status
                });
            } catch  {
                return __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$server$2e$js__$5b$app$2d$route$5d$__$28$ecmascript$29$__["NextResponse"].json({
                    detail: errorText || 'Request failed'
                }, {
                    status: response.status
                });
            }
        }
        const data = await response.json();
        return __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$server$2e$js__$5b$app$2d$route$5d$__$28$ecmascript$29$__["NextResponse"].json(data);
    } catch (error) {
        console.error('[Proxy] Unexpected error:', error.message);
        return __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$server$2e$js__$5b$app$2d$route$5d$__$28$ecmascript$29$__["NextResponse"].json({
            detail: `Failed to process request: ${error.message}`
        }, {
            status: 500
        });
    }
}
async function POST(request) {
    const pathname = request.nextUrl.pathname;
    // /api/chat/ - Send message (with trailing slash)
    if (pathname === '/api/chat' || pathname === '/api/chat/') {
        const body = await request.json();
        return proxyRequest(request, 'POST', '/api/chat/', body);
    }
    // /api/chat/conversations - Create conversation
    if (pathname === '/api/chat/conversations') {
        return proxyRequest(request, 'POST', '/api/chat/conversations');
    }
    return __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$server$2e$js__$5b$app$2d$route$5d$__$28$ecmascript$29$__["NextResponse"].json({
        detail: 'Not found'
    }, {
        status: 404
    });
}
async function GET(request) {
    const pathname = request.nextUrl.pathname;
    // /api/chat/conversations - List conversations
    if (pathname === '/api/chat/conversations') {
        return proxyRequest(request, 'GET', '/api/chat/conversations');
    }
    // /api/chat/conversations/[id]/messages - Get messages
    const messagesMatch = pathname.match(/^\/api\/chat\/conversations\/([^/]+)\/messages$/);
    if (messagesMatch) {
        const conversationId = messagesMatch[1];
        return proxyRequest(request, 'GET', `/api/chat/conversations/${conversationId}/messages`);
    }
    return __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$server$2e$js__$5b$app$2d$route$5d$__$28$ecmascript$29$__["NextResponse"].json({
        detail: 'Not found'
    }, {
        status: 404
    });
}
async function DELETE(request) {
    const pathname = request.nextUrl.pathname;
    // /api/chat/conversations/[id] - Delete conversation
    const deleteMatch = pathname.match(/^\/api\/chat\/conversations\/([^/]+)$/);
    if (deleteMatch) {
        const conversationId = deleteMatch[1];
        return proxyRequest(request, 'DELETE', `/api/chat/conversations/${conversationId}`);
    }
    return __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$server$2e$js__$5b$app$2d$route$5d$__$28$ecmascript$29$__["NextResponse"].json({
        detail: 'Not found'
    }, {
        status: 404
    });
}
}),
];

//# sourceMappingURL=%5Broot-of-the-server%5D__bec4ecd4._.js.map