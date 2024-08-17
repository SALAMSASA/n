import git
from git import Repo, GitCommandError, InvalidGitRepositoryError
import config
from ..logging import LOGGER

def update_repo():
    REPO_LINK = config.UPSTREAM_REPO
    if config.GIT_TOKEN:
        # استخراج اسم المستخدم من رابط المستودع
        GIT_USERNAME = REPO_LINK.split("com/")[1].split("/")[0]
        
        # تكوين الرابط مع التوكن الشخصي
        TEMP_REPO = REPO_LINK.split("https://")[1]
        UPSTREAM_REPO = f"https://{GIT_USERNAME}:{config.GIT_TOKEN}@{TEMP_REPO}"
    else:
        # إذا لم يكن هناك توكن، استخدم رابط المستودع كما هو
        UPSTREAM_REPO = REPO_LINK

    try:
        # محاولة فتح المستودع الحالي
        repo = Repo()
        LOGGER("Zelzal_Music").info("Git Client Found [VPS DEPLOYER]")
    except (GitCommandError, InvalidGitRepositoryError):
        # في حالة وجود خطأ في Git أو إذا كان المستودع غير صالح، نقوم بإنشاء واحد جديد
        LOGGER("Zelzal_Music").error("Invalid Git Command or Repository. Initializing a new repository.")
        repo = Repo.init()
        
        if "origin" in repo.remotes:
            origin = repo.remote("origin")
        else:
            origin = repo.create_remote("origin", UPSTREAM_REPO)

        try:
            # جلب التحديثات من الريموت "origin"
            origin.fetch()
        except GitCommandError as e:
            LOGGER("Zelzal_Music").error(f"Error fetching from remote: {e}")
            print(f"Error fetching from remote: {e}")

        # إنشاء الفرع المحلي وتتبع الفرع البعيد
        if config.UPSTREAM_BRANCH not in repo.heads:
            repo.create_head(
                config.UPSTREAM_BRANCH,
                origin.refs[config.UPSTREAM_BRANCH],
            )
        
        repo.heads[config.UPSTREAM_BRANCH].set_tracking_branch(
            origin.refs[config.UPSTREAM_BRANCH]
        )
        repo.heads[config.UPSTREAM_BRANCH].checkout(True)

    try:
        # التحقق من وجود الريموت "origin" قبل محاولة إضافته
        if "origin" not in repo.remotes:
            repo.create_remote("origin", UPSTREAM_REPO)
        origin = repo.remote("origin")
        
        try:
            # جلب التحديثات من الريموت "origin"
            origin.fetch(config.UPSTREAM_BRANCH)
            
            try:
                origin.pull(config.UPSTREAM_BRANCH)
            except GitCommandError:
                # إعادة تعيين حالة المستودع إلى حالة التحديث الأخير في حالة حدوث خطأ
                repo.git.reset("--hard", "FETCH_HEAD")
        except GitCommandError as e:
            LOGGER("Zelzal_Music").error(f"Error fetching branch from remote: {e}")
            print(f"Error fetching branch from remote: {e}")
        
        # تثبيت المتطلبات
        install_requirements("pip3 install --no-cache-dir -r requirements.txt")
        LOGGER("Zelzal_Music").info("جارِ الكشف عن تحديثات جديدة...")

    except Exception as e:
        LOGGER("Zelzal_Music").error(f"Unexpected error occurred: {e}")
        print(f"Unexpected error occurred: {e}")
