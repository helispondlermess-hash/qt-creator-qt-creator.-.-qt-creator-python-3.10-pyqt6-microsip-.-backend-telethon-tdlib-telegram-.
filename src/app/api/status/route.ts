import { NextResponse } from "next/server";

export const dynamic = "force-static";

export async function GET() {
  return NextResponse.json({
    status: "online",
    connected: false,
    timestamp: new Date().toISOString()
  });
}