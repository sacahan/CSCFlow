// 引入 Next.js 的伺服器回應工具和 Prisma ORM 客戶端
import { NextResponse } from 'next/server';
import { PrismaClient } from '@prisma/client';

// 建立 Prisma 客戶端實例，用於與資料庫互動
const prisma = new PrismaClient();

// 定義 GET 方法，用於獲取所有資料來源
export async function GET() {
  try {
    // 從資料庫中查詢所有資料來源
    const dataSources = await prisma.dataSource.findMany();
    // 將查詢結果以 JSON 格式回應
    return NextResponse.json(dataSources);
  } catch (error) {
    // 如果發生錯誤，記錄錯誤訊息並回應錯誤狀態
    console.error('Error fetching data sources:', error);
    return NextResponse.json(
      { message: '獲取資料來源時發生錯誤' }, // 錯誤訊息
      { status: 500 } // HTTP 狀態碼 500 表示伺服器錯誤
    );
  }
}

// 定義 POST 方法，用於新增資料來源
export async function POST(request) {
  try {
    // 從請求中解析 JSON 主體
    const body = await request.json();
    const { centerName, apiUrl, maxCapacity } = body;

    // 驗證請求主體中的必要欄位是否存在
    if (!centerName || !apiUrl || !maxCapacity) {
      return NextResponse.json(
        { message: '所有欄位都是必填的' }, // 錯誤訊息
        { status: 400 } // HTTP 狀態碼 400 表示用戶端錯誤
      );
    }

    // 驗證 API URL 的格式是否正確
    try {
      new URL(apiUrl); // 嘗試建立 URL 物件，若失敗則拋出錯誤
    } catch {
      return NextResponse.json(
        { message: '無效的 API URL 格式' }, // 錯誤訊息
        { status: 400 } // HTTP 狀態碼 400 表示用戶端錯誤
      );
    }

    // 使用 Prisma 在資料庫中建立新的資料來源記錄
    const dataSource = await prisma.dataSource.create({
      data: {
        centerName, // 中心名稱
        apiUrl, // API URL
        maxCapacity: parseInt(maxCapacity), // 最大容量，轉換為整數
        status: 'NORMAL' // 預設狀態為 NORMAL
      }
    });

    // 回應建立成功的資料來源記錄，並設定 HTTP 狀態碼為 201
    return NextResponse.json(dataSource, { status: 201 });
  } catch (error) {
    // 如果發生錯誤，記錄錯誤訊息並回應錯誤狀態
    console.error('Error creating data source:', error);
    return NextResponse.json(
      { message: '建立資料來源時發生錯誤' }, // 錯誤訊息
      { status: 500 } // HTTP 狀態碼 500 表示伺服器錯誤
    );
  }
}
