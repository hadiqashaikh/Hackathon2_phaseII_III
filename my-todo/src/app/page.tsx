"use client";
import React, { useState, useEffect } from "react";
import { authClient } from "@/lib/auth-client";

interface Task {
  id: string;
  title: string;
  completed: boolean;
}

export default function Dashboard() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [input, setInput] = useState("");
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");

  const { data: session, isPending } = authClient.useSession();

  useEffect(() => {
    if (session) {
      fetch("/api/tasks")
        .then((res) => res.json())
        .then((data) => {
          if (Array.isArray(data)) setTasks(data);
        });
    }
  }, [session]);

  const handleAuth = async () => {
    try {
      if (isLogin) {
        await authClient.signIn.email({ email, password });
      } else {
        await authClient.signUp.email({ email, password, name });
      }
      window.location.reload();
    } catch (err) {
      alert("Auth failed! Check credentials.");
    }
  };

  const addTask = async () => {
    if (!input.trim()) return;
    const res = await fetch("/api/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: input }),
    });
    if (res.ok) {
      const newTask = await res.json();
      setTasks((prev) => [...prev, newTask]);
      setInput("");
    }
  };

  const toggleComplete = async (task: Task) => {
    const res = await fetch("/api/tasks", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: task.id, completed: !task.completed }),
    });
    if (res.ok) {
      const updated = await res.json();
      setTasks((prev) => prev.map((t) => (t.id === task.id ? updated : t)));
    }
  };

  const editTask = async (id: string, oldTitle: string) => {
    const newTitle = prompt("Update mission:", oldTitle);
    if (!newTitle || newTitle === oldTitle) return;
    const res = await fetch("/api/tasks", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id, title: newTitle }),
    });
    if (res.ok) {
      const updated = await res.json();
      setTasks((prev) => prev.map((t) => (t.id === id ? updated : t)));
    }
  };

  const deleteTask = async (id: string) => {
    const res = await fetch("/api/tasks", {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id }),
    });
    if (res.ok) setTasks((prev) => prev.filter((t) => t.id !== id));
  };

  if (isPending) return <div style={{ color: "white", padding: "50px" }}>Loading Orbit...</div>;

  // AGAR SESSION NAHI HAI TO LOGIN SCREEN DIKHAO
  if (!session) {
    return (
      <div style={{ background: "radial-gradient(circle, #1e1b4b 0%, #000 100%)", minHeight: "100vh", display: "flex", justifyContent: "center", alignItems: "center", color: "white" }}>
        <div style={{ background: "rgba(255,255,255,0.05)", padding: "40px", borderRadius: "24px", border: "1px solid rgba(255,255,255,0.1)", backdropFilter: "blur(20px)", width: "400px" }}>
          <h2 style={{ textAlign: "center", fontSize: "2rem", marginBottom: "20px", background: "linear-gradient(to right, #60a5fa, #a855f7)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
            {isLogin ? "Orbit Login" : "Join Orbit"}
          </h2>
          {!isLogin && <input placeholder="Name" onChange={(e) => setName(e.target.value)} style={{ width: "100%", padding: "12px", margin: "10px 0", borderRadius: "10px", border: "1px solid #333", background: "#111", color: "white" }} />}
          <input placeholder="Email" onChange={(e) => setEmail(e.target.value)} style={{ width: "100%", padding: "12px", margin: "10px 0", borderRadius: "10px", border: "1px solid #333", background: "#111", color: "white" }} />
          <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} style={{ width: "100%", padding: "12px", margin: "10px 0", borderRadius: "10px", border: "1px solid #333", background: "#111", color: "white" }} />
          <button onClick={handleAuth} style={{ width: "100%", padding: "14px", background: "#2563eb", border: "none", color: "white", borderRadius: "12px", fontWeight: "bold", cursor: "pointer", marginTop: "10px" }}>
            {isLogin ? "Sign In" : "Sign Up"}
          </button>
          <p onClick={() => setIsLogin(!isLogin)} style={{ textAlign: "center", cursor: "pointer", color: "#94a3b8", marginTop: "20px" }}>
            {isLogin ? "Need an account? Sign Up" : "Back to Login"}
          </p>
        </div>
      </div>
    );
  }

  // DASHBOARD UI
  return (
    <div style={{ background: "radial-gradient(circle at 50% 50%, #1e1b4b 0%, #000000 100%)", minHeight: "100vh", padding: "40px 20px", color: "white", fontFamily: "Inter, sans-serif" }}>
      <div style={{ maxWidth: "700px", margin: "0 auto" }}>
        <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "40px" }}>
          <div>
            <h1 style={{ fontSize: "3rem", fontWeight: "900", background: "linear-gradient(to right, #60a5fa, #a855f7)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", margin: 0 }}>TASK ORBIT</h1>
            <p style={{ color: "#94a3b8" }}>Welcome back, {session?.user?.name}</p>
          </div>
          <button 
  onClick={async () => {
    const { data, error } = await authClient.signOut();
    if (!error) {
      window.location.href = "/"; 
    } else {
      window.location.replace("/");
    }
  }} 
  style={{ 
    background: "rgba(239, 68, 68, 0.2)", 
    color: "#ef4444", 
    border: "1px solid #ef4444", 
    padding: "10px 20px", 
    borderRadius: "12px", 
    cursor: "pointer", 
    fontWeight: "bold" 
  }}>
  Logout
</button>
        </header>

        <div style={{ display: "flex", gap: "12px", background: "rgba(255,255,255,0.05)", padding: "10px", borderRadius: "20px", border: "1px solid rgba(255,255,255,0.1)", backdropFilter: "blur(20px)", marginBottom: "40px" }}>
          <input value={input} onChange={(e) => setInput(e.target.value)} style={{ flex: 1, background: "transparent", border: "none", color: "white", padding: "15px", outline: "none" }} placeholder="Launch mission..." />
          <button onClick={addTask} style={{ background: "#2563eb", color: "white", padding: "0 30px", borderRadius: "14px", fontWeight: "bold", border: "none", cursor: "pointer" }}>Add</button>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "15px" }}>
          {tasks.map((task, index) => (
            <div key={task.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "18px 24px", background: "rgba(255,255,255,0.03)", borderRadius: "20px", border: "1px solid rgba(255,255,255,0.1)", animation: `fadeInUp 0.6s ease forwards ${index * 0.1}s`, opacity: 0 }}>
              <div style={{ display: "flex", alignItems: "center", gap: "18px" }}>
                <div onClick={() => toggleComplete(task)} style={{ width: "24px", height: "24px", borderRadius: "50%", border: "2px solid", borderColor: task.completed ? "#22c55e" : "#475569", background: task.completed ? "#22c55e" : "transparent", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center" }}>
                  {task.completed && <span style={{ color: "black", fontSize: "12px" }}>✓</span>}
                </div>
                <span style={{ fontSize: "17px", color: task.completed ? "#64748b" : "#f1f5f9", textDecoration: task.completed ? "line-through" : "none" }}>{task.title}</span>
              </div>
              <div style={{ display: "flex", gap: "12px" }}>
                <button onClick={() => editTask(task.id, task.title)} style={{ background: "rgba(59, 130, 246, 0.1)", border: "none", color: "#60a5fa", padding: "8px 16px", borderRadius: "12px", cursor: "pointer" }}>Edit</button>
                <button onClick={() => deleteTask(task.id)} style={{ background: "rgba(239, 68, 68, 0.1)", border: "none", color: "#ef4444", padding: "8px 16px", borderRadius: "12px", cursor: "pointer" }}>Delete</button>
              </div>
            </div>
          ))}
        </div>
      </div>
      <style jsx global>{`
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        body { background: black; margin: 0; }
      `}</style>
    </div>
  );
}