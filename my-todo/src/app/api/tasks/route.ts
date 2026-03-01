import { auth } from "@/lib/auth";
import { db } from "@/lib/db";
import { tasks } from "@/db/schema";
import { eq, and } from "drizzle-orm";
import { headers } from "next/headers";
import { NextResponse } from "next/server";

// 1. GET ALL TASKS
export async function GET() {
    const session = await auth.api.getSession({ headers: await headers() });
    if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    const userTasks = await db.select().from(tasks).where(eq(tasks.userId, session.user.id));
    return NextResponse.json(userTasks);
}

// 2. CREATE TASK
export async function POST(req: Request) {
    const session = await auth.api.getSession({ headers: await headers() });
    if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    const { title } = await req.json();
    const newTask = await db.insert(tasks).values({
        id: crypto.randomUUID(),
        userId: session.user.id,
        title,
        completed: false,
    }).returning();
    return NextResponse.json(newTask[0]);
}

// 3. UPDATE TASK (Edit & Toggle Complete) - YE WALA ZAROORI HAI!
export async function PATCH(req: Request) {
    const session = await auth.api.getSession({ headers: await headers() });
    if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

    try {
        const { id, title, completed } = await req.json();
        
        // Database mein update karo
        const updatedTask = await db.update(tasks)
            .set({ 
                ...(title !== undefined && { title }), 
                ...(completed !== undefined && { completed }) 
            })
            .where(and(eq(tasks.id, id), eq(tasks.userId, session.user.id)))
            .returning();

        return NextResponse.json(updatedTask[0]);
    } catch (error) {
        return NextResponse.json({ error: "Update failed" }, { status: 500 });
    }
}

// 4. DELETE TASK
export async function DELETE(req: Request) {
    const session = await auth.api.getSession({ headers: await headers() });
    if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    const { id } = await req.json();
    await db.delete(tasks).where(and(eq(tasks.id, id), eq(tasks.userId, session.user.id)));
    return NextResponse.json({ success: true });
}