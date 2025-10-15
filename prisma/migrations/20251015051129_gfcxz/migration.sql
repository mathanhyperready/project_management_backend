/*
  Warnings:

  - You are about to drop the column `project_id` on the `Timesheet` table. All the data in the column will be lost.
  - You are about to drop the column `user_id` on the `Timesheet` table. All the data in the column will be lost.

*/
-- DropForeignKey
ALTER TABLE "Timesheet" DROP CONSTRAINT "Timesheet_user_id_fkey";

-- AlterTable
ALTER TABLE "Timesheet" DROP COLUMN "project_id",
DROP COLUMN "user_id",
ADD COLUMN     "userId" INTEGER;

-- AddForeignKey
ALTER TABLE "Timesheet" ADD CONSTRAINT "Timesheet_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE SET NULL ON UPDATE CASCADE;
