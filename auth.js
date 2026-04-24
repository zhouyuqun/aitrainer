// 登录验证脚本
// 在每个受保护的页面引用此脚本

// 检查是否已登录，未登录则跳转到登录页
if (!localStorage.getItem('exam_logged_in')) {
    // 计算当前路径深度
    const pathname = window.location.pathname;
    // 移除文件名，获取目录路径
    const dirPath = pathname.substring(0, pathname.lastIndexOf('/'));
    // 计算目录层级数（/aitrainer/admin.html -> 1层）
    const depth = dirPath.split('/').filter(p => p).length - 1;
    // 生成返回根目录的路径
    const prefix = '../'.repeat(depth);
    // 跳转到根目录的 login.html
    window.location.href = prefix + 'login.html';
}
