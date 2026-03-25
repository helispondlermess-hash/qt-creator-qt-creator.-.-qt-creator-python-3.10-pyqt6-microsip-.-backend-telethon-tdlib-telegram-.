import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    status: "online",
    connected: false,
    timestamp: new Date().toISOString()
  });
}