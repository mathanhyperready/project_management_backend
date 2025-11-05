/*
  Warnings:

  - You are about to drop the `Client` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `Permission` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `Project` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `Role` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `Timesheet` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `User` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `_RolePermissions` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE "Client" DROP CONSTRAINT "Client_created_by_fkey";

-- DropForeignKey
ALTER TABLE "Project" DROP CONSTRAINT "Project_client_id_fkey";

-- DropForeignKey
ALTER TABLE "Project" DROP CONSTRAINT "Project_created_by_fkey";

-- DropForeignKey
ALTER TABLE "Project" DROP CONSTRAINT "Project_user_id_fkey";

-- DropForeignKey
ALTER TABLE "Role" DROP CONSTRAINT "Role_created_by_fkey";

-- DropForeignKey
ALTER TABLE "Timesheet" DROP CONSTRAINT "Timesheet_created_by_fkey";

-- DropForeignKey
ALTER TABLE "Timesheet" DROP CONSTRAINT "Timesheet_projectId_fkey";

-- DropForeignKey
ALTER TABLE "Timesheet" DROP CONSTRAINT "Timesheet_userId_fkey";

-- DropForeignKey
ALTER TABLE "User" DROP CONSTRAINT "User_role_id_fkey";

-- DropForeignKey
ALTER TABLE "_RolePermissions" DROP CONSTRAINT "_RolePermissions_A_fkey";

-- DropForeignKey
ALTER TABLE "_RolePermissions" DROP CONSTRAINT "_RolePermissions_B_fkey";

-- DropTable
DROP TABLE "Client";

-- DropTable
DROP TABLE "Permission";

-- DropTable
DROP TABLE "Project";

-- DropTable
DROP TABLE "Role";

-- DropTable
DROP TABLE "Timesheet";

-- DropTable
DROP TABLE "User";

-- DropTable
DROP TABLE "_RolePermissions";

-- CreateTable
CREATE TABLE "users" (
    "id" SERIAL NOT NULL,
    "user_name" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "rolename" TEXT,
    "status" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_active" BOOLEAN NOT NULL DEFAULT true,
    "role_id" INTEGER,
    "created_by" INTEGER,

    CONSTRAINT "users_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "roles" (
    "id" SERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "is_enabled" BOOLEAN NOT NULL DEFAULT true,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "created_by" INTEGER,

    CONSTRAINT "roles_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "permissions" (
    "id" SERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,
    "is_enabled" BOOLEAN NOT NULL DEFAULT true,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "role_id" INTEGER,

    CONSTRAINT "permissions_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "projects" (
    "id" SERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,
    "start_date" TIMESTAMP(3) NOT NULL,
    "end_date" TIMESTAMP(3) NOT NULL,
    "status" "ProjectStatus" NOT NULL DEFAULT 'PLANNED',
    "created_by" INTEGER,

    CONSTRAINT "projects_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "timesheets" (
    "id" SERIAL NOT NULL,
    "description" TEXT NOT NULL,
    "start_date" TIMESTAMP(3) NOT NULL,
    "end_date" TIMESTAMP(3) NOT NULL,
    "duration" INTEGER NOT NULL,
    "status" "TimesheetStatus" NOT NULL DEFAULT 'PENDING',
    "projectId" INTEGER,
    "userId" INTEGER,
    "created_by" INTEGER,

    CONSTRAINT "timesheets_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "users" ADD CONSTRAINT "users_role_id_fkey" FOREIGN KEY ("role_id") REFERENCES "roles"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "roles" ADD CONSTRAINT "roles_created_by_fkey" FOREIGN KEY ("created_by") REFERENCES "users"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "permissions" ADD CONSTRAINT "permissions_role_id_fkey" FOREIGN KEY ("role_id") REFERENCES "roles"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "projects" ADD CONSTRAINT "projects_created_by_fkey" FOREIGN KEY ("created_by") REFERENCES "users"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "timesheets" ADD CONSTRAINT "timesheets_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "timesheets" ADD CONSTRAINT "timesheets_userId_fkey" FOREIGN KEY ("userId") REFERENCES "users"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "timesheets" ADD CONSTRAINT "timesheets_created_by_fkey" FOREIGN KEY ("created_by") REFERENCES "users"("id") ON DELETE SET NULL ON UPDATE CASCADE;
