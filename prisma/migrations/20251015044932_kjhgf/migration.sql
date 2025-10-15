-- DropForeignKey
ALTER TABLE "Timesheet" DROP CONSTRAINT "Timesheet_project_id_fkey";

-- AlterTable
ALTER TABLE "Timesheet" ADD COLUMN     "projectId" INTEGER;

-- AddForeignKey
ALTER TABLE "Timesheet" ADD CONSTRAINT "Timesheet_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "Project"("id") ON DELETE SET NULL ON UPDATE CASCADE;
