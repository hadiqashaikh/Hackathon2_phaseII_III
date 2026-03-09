(globalThis.TURBOPACK || (globalThis.TURBOPACK = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/src/lib/auth-client.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "authClient",
    ()=>authClient
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$better$2d$auth$2f$dist$2f$client$2f$react$2f$index$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$locals$3e$__ = __turbopack_context__.i("[project]/node_modules/better-auth/dist/client/react/index.mjs [app-client] (ecmascript) <locals>");
;
const authClient = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$better$2d$auth$2f$dist$2f$client$2f$react$2f$index$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$locals$3e$__["createAuthClient"])({
    baseURL: __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
    fetchOptions: {
        credentials: 'include'
    }
});
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/src/app/page.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>Dashboard
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$styled$2d$jsx$2f$style$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/styled-jsx/style.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$compiler$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/compiler-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$auth$2d$client$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/lib/auth-client.ts [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
"use client";
;
;
;
;
function Dashboard() {
    _s();
    const $ = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$compiler$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["c"])(76);
    if ($[0] !== "6bb28d0f4070743ca88811ea8b387afa0ba049a70ca5a967dc1a0fdbc1c8cd27") {
        for(let $i = 0; $i < 76; $i += 1){
            $[$i] = Symbol.for("react.memo_cache_sentinel");
        }
        $[0] = "6bb28d0f4070743ca88811ea8b387afa0ba049a70ca5a967dc1a0fdbc1c8cd27";
    }
    let t0;
    if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
        t0 = [];
        $[1] = t0;
    } else {
        t0 = $[1];
    }
    const [tasks, setTasks] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(t0);
    const [input, setInput] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [isLogin, setIsLogin] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(true);
    const [email, setEmail] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [password, setPassword] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [name, setName] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const { data: session, isPending } = __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$auth$2d$client$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["authClient"].useSession();
    let t1;
    let t2;
    if ($[2] !== session) {
        t1 = ({
            "Dashboard[useEffect()]": ()=>{
                if (session) {
                    fetch("/api/tasks").then(_DashboardUseEffectAnonymous).then({
                        "Dashboard[useEffect() > (anonymous)()]": (data)=>{
                            if (Array.isArray(data)) {
                                setTasks(data);
                            }
                        }
                    }["Dashboard[useEffect() > (anonymous)()]"]);
                }
            }
        })["Dashboard[useEffect()]"];
        t2 = [
            session
        ];
        $[2] = session;
        $[3] = t1;
        $[4] = t2;
    } else {
        t1 = $[3];
        t2 = $[4];
    }
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])(t1, t2);
    let t3;
    if ($[5] !== email || $[6] !== isLogin || $[7] !== name || $[8] !== password) {
        t3 = ({
            "Dashboard[handleAuth]": async ()=>{
                ;
                try {
                    if (isLogin) {
                        await __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$auth$2d$client$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["authClient"].signIn.email({
                            email,
                            password
                        });
                    } else {
                        await __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$auth$2d$client$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["authClient"].signUp.email({
                            email,
                            password,
                            name
                        });
                    }
                    window.location.reload();
                } catch (t4) {
                    alert("Auth failed! Check credentials.");
                }
            }
        })["Dashboard[handleAuth]"];
        $[5] = email;
        $[6] = isLogin;
        $[7] = name;
        $[8] = password;
        $[9] = t3;
    } else {
        t3 = $[9];
    }
    const handleAuth = t3;
    let t4;
    if ($[10] !== input) {
        t4 = ({
            "Dashboard[addTask]": async ()=>{
                if (!input.trim()) {
                    return;
                }
                const res_0 = await fetch("/api/tasks", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        title: input
                    })
                });
                if (res_0.ok) {
                    const newTask = await res_0.json();
                    setTasks({
                        "Dashboard[addTask > setTasks()]": (prev)=>[
                                ...prev,
                                newTask
                            ]
                    }["Dashboard[addTask > setTasks()]"]);
                    setInput("");
                }
            }
        })["Dashboard[addTask]"];
        $[10] = input;
        $[11] = t4;
    } else {
        t4 = $[11];
    }
    const addTask = t4;
    let t5;
    if ($[12] === Symbol.for("react.memo_cache_sentinel")) {
        t5 = ({
            "Dashboard[toggleComplete]": async (task)=>{
                const res_1 = await fetch("/api/tasks", {
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        id: task.id,
                        completed: !task.completed
                    })
                });
                if (res_1.ok) {
                    const updated = await res_1.json();
                    setTasks({
                        "Dashboard[toggleComplete > setTasks()]": (prev_0)=>prev_0.map({
                                "Dashboard[toggleComplete > setTasks() > prev_0.map()]": (t)=>t.id === task.id ? updated : t
                            }["Dashboard[toggleComplete > setTasks() > prev_0.map()]"])
                    }["Dashboard[toggleComplete > setTasks()]"]);
                }
            }
        })["Dashboard[toggleComplete]"];
        $[12] = t5;
    } else {
        t5 = $[12];
    }
    const toggleComplete = t5;
    let t6;
    if ($[13] === Symbol.for("react.memo_cache_sentinel")) {
        t6 = ({
            "Dashboard[editTask]": async (id, oldTitle)=>{
                const newTitle = prompt("Update mission:", oldTitle);
                if (!newTitle || newTitle === oldTitle) {
                    return;
                }
                const res_2 = await fetch("/api/tasks", {
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        id,
                        title: newTitle
                    })
                });
                if (res_2.ok) {
                    const updated_0 = await res_2.json();
                    setTasks({
                        "Dashboard[editTask > setTasks()]": (prev_1)=>prev_1.map({
                                "Dashboard[editTask > setTasks() > prev_1.map()]": (t_0)=>t_0.id === id ? updated_0 : t_0
                            }["Dashboard[editTask > setTasks() > prev_1.map()]"])
                    }["Dashboard[editTask > setTasks()]"]);
                }
            }
        })["Dashboard[editTask]"];
        $[13] = t6;
    } else {
        t6 = $[13];
    }
    const editTask = t6;
    let t7;
    if ($[14] === Symbol.for("react.memo_cache_sentinel")) {
        t7 = ({
            "Dashboard[deleteTask]": async (id_0)=>{
                const res_3 = await fetch("/api/tasks", {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        id: id_0
                    })
                });
                if (res_3.ok) {
                    setTasks({
                        "Dashboard[deleteTask > setTasks()]": (prev_2)=>prev_2.filter({
                                "Dashboard[deleteTask > setTasks() > prev_2.filter()]": (t_1)=>t_1.id !== id_0
                            }["Dashboard[deleteTask > setTasks() > prev_2.filter()]"])
                    }["Dashboard[deleteTask > setTasks()]"]);
                }
            }
        })["Dashboard[deleteTask]"];
        $[14] = t7;
    } else {
        t7 = $[14];
    }
    const deleteTask = t7;
    if (isPending) {
        let t8;
        if ($[15] === Symbol.for("react.memo_cache_sentinel")) {
            t8 = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                style: {
                    color: "white",
                    padding: "50px"
                },
                children: "Loading Orbit..."
            }, void 0, false, {
                fileName: "[project]/src/app/page.tsx",
                lineNumber: 217,
                columnNumber: 12
            }, this);
            $[15] = t8;
        } else {
            t8 = $[15];
        }
        return t8;
    }
    if (!session) {
        let t10;
        let t8;
        let t9;
        if ($[16] === Symbol.for("react.memo_cache_sentinel")) {
            t8 = {
                background: "radial-gradient(circle, #1e1b4b 0%, #000 100%)",
                minHeight: "100vh",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                color: "white"
            };
            t9 = {
                background: "rgba(255,255,255,0.05)",
                padding: "40px",
                borderRadius: "24px",
                border: "1px solid rgba(255,255,255,0.1)",
                backdropFilter: "blur(20px)",
                width: "400px"
            };
            t10 = {
                textAlign: "center",
                fontSize: "2rem",
                marginBottom: "20px",
                background: "linear-gradient(to right, #60a5fa, #a855f7)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent"
            };
            $[16] = t10;
            $[17] = t8;
            $[18] = t9;
        } else {
            t10 = $[16];
            t8 = $[17];
            t9 = $[18];
        }
        const t11 = isLogin ? "Orbit Login" : "Join Orbit";
        let t12;
        if ($[19] !== t11) {
            t12 = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                style: t10,
                children: t11
            }, void 0, false, {
                fileName: "[project]/src/app/page.tsx",
                lineNumber: 267,
                columnNumber: 13
            }, this);
            $[19] = t11;
            $[20] = t12;
        } else {
            t12 = $[20];
        }
        let t13;
        if ($[21] !== isLogin) {
            t13 = !isLogin && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                placeholder: "Name",
                onChange: {
                    "Dashboard[<input>.onChange]": (e)=>setName(e.target.value)
                }["Dashboard[<input>.onChange]"],
                style: {
                    width: "100%",
                    padding: "12px",
                    margin: "10px 0",
                    borderRadius: "10px",
                    border: "1px solid #333",
                    background: "#111",
                    color: "white"
                }
            }, void 0, false, {
                fileName: "[project]/src/app/page.tsx",
                lineNumber: 275,
                columnNumber: 25
            }, this);
            $[21] = isLogin;
            $[22] = t13;
        } else {
            t13 = $[22];
        }
        let t14;
        if ($[23] === Symbol.for("react.memo_cache_sentinel")) {
            t14 = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                placeholder: "Email",
                onChange: {
                    "Dashboard[<input>.onChange]": (e_0)=>setEmail(e_0.target.value)
                }["Dashboard[<input>.onChange]"],
                style: {
                    width: "100%",
                    padding: "12px",
                    margin: "10px 0",
                    borderRadius: "10px",
                    border: "1px solid #333",
                    background: "#111",
                    color: "white"
                }
            }, void 0, false, {
                fileName: "[project]/src/app/page.tsx",
                lineNumber: 293,
                columnNumber: 13
            }, this);
            $[23] = t14;
        } else {
            t14 = $[23];
        }
        let t15;
        if ($[24] === Symbol.for("react.memo_cache_sentinel")) {
            t15 = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                type: "password",
                placeholder: "Password",
                onChange: {
                    "Dashboard[<input>.onChange]": (e_1)=>setPassword(e_1.target.value)
                }["Dashboard[<input>.onChange]"],
                style: {
                    width: "100%",
                    padding: "12px",
                    margin: "10px 0",
                    borderRadius: "10px",
                    border: "1px solid #333",
                    background: "#111",
                    color: "white"
                }
            }, void 0, false, {
                fileName: "[project]/src/app/page.tsx",
                lineNumber: 310,
                columnNumber: 13
            }, this);
            $[24] = t15;
        } else {
            t15 = $[24];
        }
        let t16;
        if ($[25] === Symbol.for("react.memo_cache_sentinel")) {
            t16 = {
                width: "100%",
                padding: "14px",
                background: "#2563eb",
                border: "none",
                color: "white",
                borderRadius: "12px",
                fontWeight: "bold",
                cursor: "pointer",
                marginTop: "10px"
            };
            $[25] = t16;
        } else {
            t16 = $[25];
        }
        const t17 = isLogin ? "Sign In" : "Sign Up";
        let t18;
        if ($[26] !== handleAuth || $[27] !== t17) {
            t18 = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                onClick: handleAuth,
                style: t16,
                children: t17
            }, void 0, false, {
                fileName: "[project]/src/app/page.tsx",
                lineNumber: 345,
                columnNumber: 13
            }, this);
            $[26] = handleAuth;
            $[27] = t17;
            $[28] = t18;
        } else {
            t18 = $[28];
        }
        let t19;
        if ($[29] !== isLogin) {
            t19 = ({
                "Dashboard[<p>.onClick]": ()=>setIsLogin(!isLogin)
            })["Dashboard[<p>.onClick]"];
            $[29] = isLogin;
            $[30] = t19;
        } else {
            t19 = $[30];
        }
        let t20;
        if ($[31] === Symbol.for("react.memo_cache_sentinel")) {
            t20 = {
                textAlign: "center",
                cursor: "pointer",
                color: "#94a3b8",
                marginTop: "20px"
            };
            $[31] = t20;
        } else {
            t20 = $[31];
        }
        const t21 = isLogin ? "Need an account? Sign Up" : "Back to Login";
        let t22;
        if ($[32] !== t19 || $[33] !== t21) {
            t22 = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                onClick: t19,
                style: t20,
                children: t21
            }, void 0, false, {
                fileName: "[project]/src/app/page.tsx",
                lineNumber: 377,
                columnNumber: 13
            }, this);
            $[32] = t19;
            $[33] = t21;
            $[34] = t22;
        } else {
            t22 = $[34];
        }
        let t23;
        if ($[35] !== t12 || $[36] !== t13 || $[37] !== t18 || $[38] !== t22) {
            t23 = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                style: t8,
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    style: t9,
                    children: [
                        t12,
                        t13,
                        t14,
                        t15,
                        t18,
                        t22
                    ]
                }, void 0, true, {
                    fileName: "[project]/src/app/page.tsx",
                    lineNumber: 386,
                    columnNumber: 29
                }, this)
            }, void 0, false, {
                fileName: "[project]/src/app/page.tsx",
                lineNumber: 386,
                columnNumber: 13
            }, this);
            $[35] = t12;
            $[36] = t13;
            $[37] = t18;
            $[38] = t22;
            $[39] = t23;
        } else {
            t23 = $[39];
        }
        return t23;
    }
    let t10;
    let t11;
    let t12;
    let t8;
    let t9;
    if ($[40] === Symbol.for("react.memo_cache_sentinel")) {
        t8 = {
            background: "radial-gradient(circle at 50% 50%, #1e1b4b 0%, #000000 100%)",
            minHeight: "100vh",
            padding: "40px 20px",
            color: "white",
            fontFamily: "Inter, sans-serif"
        };
        t9 = {
            maxWidth: "700px",
            margin: "0 auto"
        };
        t10 = {
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "40px"
        };
        t11 = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
            style: {
                fontSize: "3rem",
                fontWeight: "900",
                background: "linear-gradient(to right, #60a5fa, #a855f7)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
                margin: 0
            },
            children: "TASK ORBIT"
        }, void 0, false, {
            fileName: "[project]/src/app/page.tsx",
            lineNumber: 420,
            columnNumber: 11
        }, this);
        t12 = {
            color: "#94a3b8"
        };
        $[40] = t10;
        $[41] = t11;
        $[42] = t12;
        $[43] = t8;
        $[44] = t9;
    } else {
        t10 = $[40];
        t11 = $[41];
        t12 = $[42];
        t8 = $[43];
        t9 = $[44];
    }
    const t13 = session?.user?.name;
    let t14;
    if ($[45] !== t13) {
        t14 = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            children: [
                t11,
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                    style: t12,
                    children: [
                        "Welcome back, ",
                        t13
                    ]
                }, void 0, true, {
                    fileName: "[project]/src/app/page.tsx",
                    lineNumber: 446,
                    columnNumber: 21
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/src/app/page.tsx",
            lineNumber: 446,
            columnNumber: 11
        }, this);
        $[45] = t13;
        $[46] = t14;
    } else {
        t14 = $[46];
    }
    let t15;
    if ($[47] === Symbol.for("react.memo_cache_sentinel")) {
        t15 = {
            display: "flex",
            gap: "10px"
        };
        $[47] = t15;
    } else {
        t15 = $[47];
    }
    let t16;
    if ($[48] === Symbol.for("react.memo_cache_sentinel")) {
        t16 = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("a", {
            href: "/chat",
            style: {
                background: "rgba(37, 99, 235, 0.2)",
                color: "#60a5fa",
                border: "1px solid #3b82f6",
                padding: "10px 20px",
                borderRadius: "12px",
                cursor: "pointer",
                fontWeight: "bold",
                textDecoration: "none",
                display: "flex",
                alignItems: "center",
                gap: "8px"
            },
            children: "🤖 AI Chat"
        }, void 0, false, {
            fileName: "[project]/src/app/page.tsx",
            lineNumber: 464,
            columnNumber: 11
        }, this);
        $[48] = t16;
    } else {
        t16 = $[48];
    }
    let t17;
    if ($[49] === Symbol.for("react.memo_cache_sentinel")) {
        t17 = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            style: t15,
            children: [
                t16,
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                    onClick: _DashboardButtonOnClick,
                    style: {
                        background: "rgba(239, 68, 68, 0.2)",
                        color: "#ef4444",
                        border: "1px solid #ef4444",
                        padding: "10px 20px",
                        borderRadius: "12px",
                        cursor: "pointer",
                        fontWeight: "bold"
                    },
                    children: "Logout"
                }, void 0, false, {
                    fileName: "[project]/src/app/page.tsx",
                    lineNumber: 483,
                    columnNumber: 33
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/src/app/page.tsx",
            lineNumber: 483,
            columnNumber: 11
        }, this);
        $[49] = t17;
    } else {
        t17 = $[49];
    }
    let t18;
    if ($[50] !== t14) {
        t18 = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("header", {
            style: t10,
            children: [
                t14,
                t17
            ]
        }, void 0, true, {
            fileName: "[project]/src/app/page.tsx",
            lineNumber: 498,
            columnNumber: 11
        }, this);
        $[50] = t14;
        $[51] = t18;
    } else {
        t18 = $[51];
    }
    let t19;
    if ($[52] === Symbol.for("react.memo_cache_sentinel")) {
        t19 = {
            display: "flex",
            gap: "12px",
            background: "rgba(255,255,255,0.05)",
            padding: "10px",
            borderRadius: "20px",
            border: "1px solid rgba(255,255,255,0.1)",
            backdropFilter: "blur(20px)",
            marginBottom: "40px"
        };
        $[52] = t19;
    } else {
        t19 = $[52];
    }
    let t20;
    let t21;
    if ($[53] === Symbol.for("react.memo_cache_sentinel")) {
        t20 = ({
            "Dashboard[<input>.onChange]": (e_2)=>setInput(e_2.target.value)
        })["Dashboard[<input>.onChange]"];
        t21 = {
            flex: 1,
            background: "transparent",
            border: "none",
            color: "white",
            padding: "15px",
            outline: "none"
        };
        $[53] = t20;
        $[54] = t21;
    } else {
        t20 = $[53];
        t21 = $[54];
    }
    let t22;
    if ($[55] !== input) {
        t22 = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
            value: input,
            onChange: t20,
            style: t21,
            placeholder: "Launch mission..."
        }, void 0, false, {
            fileName: "[project]/src/app/page.tsx",
            lineNumber: 542,
            columnNumber: 11
        }, this);
        $[55] = input;
        $[56] = t22;
    } else {
        t22 = $[56];
    }
    let t23;
    if ($[57] === Symbol.for("react.memo_cache_sentinel")) {
        t23 = {
            background: "#2563eb",
            color: "white",
            padding: "0 30px",
            borderRadius: "14px",
            fontWeight: "bold",
            border: "none",
            cursor: "pointer"
        };
        $[57] = t23;
    } else {
        t23 = $[57];
    }
    let t24;
    if ($[58] !== addTask) {
        t24 = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
            onClick: addTask,
            style: t23,
            children: "Add"
        }, void 0, false, {
            fileName: "[project]/src/app/page.tsx",
            lineNumber: 565,
            columnNumber: 11
        }, this);
        $[58] = addTask;
        $[59] = t24;
    } else {
        t24 = $[59];
    }
    let t25;
    if ($[60] !== t22 || $[61] !== t24) {
        t25 = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            style: t19,
            children: [
                t22,
                t24
            ]
        }, void 0, true, {
            fileName: "[project]/src/app/page.tsx",
            lineNumber: 573,
            columnNumber: 11
        }, this);
        $[60] = t22;
        $[61] = t24;
        $[62] = t25;
    } else {
        t25 = $[62];
    }
    let t26;
    if ($[63] === Symbol.for("react.memo_cache_sentinel")) {
        t26 = {
            display: "flex",
            flexDirection: "column",
            gap: "15px"
        };
        $[63] = t26;
    } else {
        t26 = $[63];
    }
    let t27;
    if ($[64] !== tasks) {
        let t28;
        if ($[66] === Symbol.for("react.memo_cache_sentinel")) {
            t28 = ({
                "Dashboard[tasks.map()]": (task_0, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "center",
                            padding: "18px 24px",
                            background: "rgba(255,255,255,0.03)",
                            borderRadius: "20px",
                            border: "1px solid rgba(255,255,255,0.1)",
                            animation: `fadeInUp 0.6s ease forwards ${index * 0.1}s`,
                            opacity: 0
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    display: "flex",
                                    alignItems: "center",
                                    gap: "18px"
                                },
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        onClick: {
                                            "Dashboard[tasks.map() > <div>.onClick]": ()=>toggleComplete(task_0)
                                        }["Dashboard[tasks.map() > <div>.onClick]"],
                                        style: {
                                            width: "24px",
                                            height: "24px",
                                            borderRadius: "50%",
                                            border: "2px solid",
                                            borderColor: task_0.completed ? "#22c55e" : "#475569",
                                            background: task_0.completed ? "#22c55e" : "transparent",
                                            cursor: "pointer",
                                            display: "flex",
                                            alignItems: "center",
                                            justifyContent: "center"
                                        },
                                        children: task_0.completed && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                            style: {
                                                color: "black",
                                                fontSize: "12px"
                                            },
                                            children: "✓"
                                        }, void 0, false, {
                                            fileName: "[project]/src/app/page.tsx",
                                            lineNumber: 623,
                                            columnNumber: 37
                                        }, this)
                                    }, void 0, false, {
                                        fileName: "[project]/src/app/page.tsx",
                                        lineNumber: 610,
                                        columnNumber: 14
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        style: {
                                            fontSize: "17px",
                                            color: task_0.completed ? "#64748b" : "#f1f5f9",
                                            textDecoration: task_0.completed ? "line-through" : "none"
                                        },
                                        children: task_0.title
                                    }, void 0, false, {
                                        fileName: "[project]/src/app/page.tsx",
                                        lineNumber: 626,
                                        columnNumber: 33
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/app/page.tsx",
                                lineNumber: 606,
                                columnNumber: 12
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    display: "flex",
                                    gap: "12px"
                                },
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        onClick: {
                                            "Dashboard[tasks.map() > <button>.onClick]": ()=>editTask(task_0.id, task_0.title)
                                        }["Dashboard[tasks.map() > <button>.onClick]"],
                                        style: {
                                            background: "rgba(59, 130, 246, 0.1)",
                                            border: "none",
                                            color: "#60a5fa",
                                            padding: "8px 16px",
                                            borderRadius: "12px",
                                            cursor: "pointer"
                                        },
                                        children: "Edit"
                                    }, void 0, false, {
                                        fileName: "[project]/src/app/page.tsx",
                                        lineNumber: 633,
                                        columnNumber: 14
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        onClick: {
                                            "Dashboard[tasks.map() > <button>.onClick]": ()=>deleteTask(task_0.id)
                                        }["Dashboard[tasks.map() > <button>.onClick]"],
                                        style: {
                                            background: "rgba(239, 68, 68, 0.1)",
                                            border: "none",
                                            color: "#ef4444",
                                            padding: "8px 16px",
                                            borderRadius: "12px",
                                            cursor: "pointer"
                                        },
                                        children: "Delete"
                                    }, void 0, false, {
                                        fileName: "[project]/src/app/page.tsx",
                                        lineNumber: 642,
                                        columnNumber: 29
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/app/page.tsx",
                                lineNumber: 630,
                                columnNumber: 43
                            }, this)
                        ]
                    }, task_0.id, true, {
                        fileName: "[project]/src/app/page.tsx",
                        lineNumber: 596,
                        columnNumber: 54
                    }, this)
            })["Dashboard[tasks.map()]"];
            $[66] = t28;
        } else {
            t28 = $[66];
        }
        t27 = tasks.map(t28);
        $[64] = tasks;
        $[65] = t27;
    } else {
        t27 = $[65];
    }
    let t28;
    if ($[67] !== t27) {
        t28 = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            style: t26,
            children: t27
        }, void 0, false, {
            fileName: "[project]/src/app/page.tsx",
            lineNumber: 665,
            columnNumber: 11
        }, this);
        $[67] = t27;
        $[68] = t28;
    } else {
        t28 = $[68];
    }
    let t29;
    if ($[69] !== t18 || $[70] !== t25 || $[71] !== t28) {
        t29 = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            style: t9,
            children: [
                t18,
                t25,
                t28
            ]
        }, void 0, true, {
            fileName: "[project]/src/app/page.tsx",
            lineNumber: 673,
            columnNumber: 11
        }, this);
        $[69] = t18;
        $[70] = t25;
        $[71] = t28;
        $[72] = t29;
    } else {
        t29 = $[72];
    }
    let t30;
    if ($[73] === Symbol.for("react.memo_cache_sentinel")) {
        t30 = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$styled$2d$jsx$2f$style$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
            id: "16cd94f44d99ad6d",
            children: "@keyframes fadeInUp{0%{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}body{background:#000;margin:0}"
        }, void 0, false, void 0, this);
        $[73] = t30;
    } else {
        t30 = $[73];
    }
    let t31;
    if ($[74] !== t29) {
        t31 = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            style: t8,
            children: [
                t29,
                t30
            ]
        }, void 0, true, {
            fileName: "[project]/src/app/page.tsx",
            lineNumber: 690,
            columnNumber: 11
        }, this);
        $[74] = t29;
        $[75] = t31;
    } else {
        t31 = $[75];
    }
    return t31;
}
_s(Dashboard, "glXJhNIDvFraUx0+D5U9GInwbgc=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$auth$2d$client$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["authClient"].useSession
    ];
});
_c = Dashboard;
async function _DashboardButtonOnClick() {
    const { error } = await __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$auth$2d$client$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["authClient"].signOut();
    if (!error) {
        window.location.href = "/";
    } else {
        window.location.replace("/");
    }
}
function _DashboardUseEffectAnonymous(res) {
    return res.json();
}
var _c;
__turbopack_context__.k.register(_c, "Dashboard");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
]);

//# sourceMappingURL=src_ed7b28d5._.js.map