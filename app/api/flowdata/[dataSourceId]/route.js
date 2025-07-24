import { NextResponse } from 'next/server';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

/**
 * 處理 GET 請求以獲取指定資料來源的流量數據
 * @param {Request} request - 請求物件
 * @param {Object} context - 上下文物件，包含路由參數
 * @returns {Response} - 包含流量數據的 JSON 回應
 */
export async function GET(request, context) {
    try {
        // 從 context 中解構 params 並解析 dataSourceId
        const params = await context.params;
        const dataSourceId = parseInt(params.dataSourceId, 10); // 確保轉換為整數

        // 從資料庫中查詢最近 24 筆流量數據，按時間戳降序排列
        const flowData = await prisma.flowData.findMany({
            where: {
                dataSourceId, // 使用轉換後的 dataSourceId
            },
            orderBy: {
                timestamp: 'desc', // 按時間戳降序排列
            },
            take: 24, // 取得最近 24 筆資料
        });

        // 回應查詢結果，設定 HTTP 狀態碼為 200
        return NextResponse.json(flowData, {
            status: 200,
        });
    } catch (error) {
        // 如果發生錯誤，記錄錯誤訊息並回應錯誤狀態
        console.error('Error fetching flow data:', error);
        return NextResponse.json(
            { error: 'Internal Server Error' }, // 錯誤訊息
            { status: 500 } // HTTP 狀態碼 500 表示伺服器錯誤
        );
    }
}
