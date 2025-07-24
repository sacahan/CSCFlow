-- CreateTable
CREATE TABLE "DataSource" (
    "id" SERIAL NOT NULL,
    "centerName" TEXT NOT NULL,
    "apiUrl" TEXT NOT NULL,
    "maxCapacity" INTEGER NOT NULL,
    "status" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "DataSource_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "FlowData" (
    "id" SERIAL NOT NULL,
    "currentCount" INTEGER NOT NULL,
    "timestamp" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "dataSourceId" INTEGER NOT NULL,

    CONSTRAINT "FlowData_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "FlowData" ADD CONSTRAINT "FlowData_dataSourceId_fkey" FOREIGN KEY ("dataSourceId") REFERENCES "DataSource"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
