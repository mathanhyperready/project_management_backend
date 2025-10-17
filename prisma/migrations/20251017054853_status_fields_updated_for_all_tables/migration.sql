/*
  Warnings:

  - The `status` column on the `Timesheet` table would be dropped and recreated. This will lead to data loss if there is data in the column.

*/
-- CreateEnum
CREATE TYPE "ProjectStatus" AS ENUM ('PLANNED', 'IN_PROGRESS', 'COMPLETED', 'ON_HOLD', 'CANCELLED');

-- CreateEnum
CREATE TYPE "TimesheetStatus" AS ENUM ('PENDING', 'APPROVED', 'REJECTED');

-- AlterTable
ALTER TABLE "Client" ADD COLUMN     "is_enabled" BOOLEAN NOT NULL DEFAULT true;

-- AlterTable
ALTER TABLE "Project" ADD COLUMN     "status" "ProjectStatus" NOT NULL DEFAULT 'PLANNED';

-- AlterTable
ALTER TABLE "Role" ADD COLUMN     "is_enabled" BOOLEAN NOT NULL DEFAULT true;

-- AlterTable
ALTER TABLE "Timesheet" DROP COLUMN "status",
ADD COLUMN     "status" "TimesheetStatus" NOT NULL DEFAULT 'PENDING';

-- AlterTable
ALTER TABLE "User" ADD COLUMN     "is_active" BOOLEAN NOT NULL DEFAULT true;
