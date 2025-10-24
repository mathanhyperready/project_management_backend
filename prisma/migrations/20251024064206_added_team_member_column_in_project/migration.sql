/*
  Warnings:

  - You are about to drop the `ProjectTeamMember` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE "ProjectTeamMember" DROP CONSTRAINT "ProjectTeamMember_project_id_fkey";

-- DropForeignKey
ALTER TABLE "ProjectTeamMember" DROP CONSTRAINT "ProjectTeamMember_user_id_fkey";

-- AlterTable
ALTER TABLE "Project" ADD COLUMN     "teamMembers" TEXT[];

-- DropTable
DROP TABLE "ProjectTeamMember";
