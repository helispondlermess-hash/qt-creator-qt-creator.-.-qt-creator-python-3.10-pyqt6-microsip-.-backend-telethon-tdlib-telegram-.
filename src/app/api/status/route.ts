import { NextResponse } from "next/server";

const API_URL = process.env.API_URL || "http://localhost:8080";

export async function POST() {
  try {
    const res = await fetch(`${API_URL}/api/status`);
    const data = await res.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ status: "offline", error: "Server not available" }, { status: 503 });
  }
}