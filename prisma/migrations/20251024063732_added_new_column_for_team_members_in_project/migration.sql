-- CreateTable
CREATE TABLE "ProjectTeamMember" (
    "id" SERIAL NOT NULL,
    "project_id" INTEGER NOT NULL,
    "user_id" INTEGER NOT NULL,
    "role" TEXT,
    "added_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "ProjectTeamMember_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "ProjectTeamMember_project_id_idx" ON "ProjectTeamMember"("project_id");

-- CreateIndex
CREATE INDEX "ProjectTeamMember_user_id_idx" ON "ProjectTeamMember"("user_id");

-- CreateIndex
CREATE UNIQUE INDEX "ProjectTeamMember_project_id_user_id_key" ON "ProjectTeamMember"("project_id", "user_id");

-- AddForeignKey
ALTER TABLE "ProjectTeamMember" ADD CONSTRAINT "ProjectTeamMember_project_id_fkey" FOREIGN KEY ("project_id") REFERENCES "Project"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "ProjectTeamMember" ADD CONSTRAINT "ProjectTeamMember_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "User"("id") ON DELETE CASCADE ON UPDATE CASCADE;
