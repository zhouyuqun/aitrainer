// 登录验证脚本
// 在每个受保护的页面引用此脚本

// 检查是否已登录，未登录则跳转到登录页
if (!localStorage.getItem('exam_logged_in')) {
    // 获取当前页面深度，自动确定 login.html 的相对路径
    const pathParts = window.location.pathname.split('/').filter(p => p && p !== 'index.html');
    const depth = pathParts.length - 1; // 去掉文件名本身
    const prefix = '../'.repeat(depth);
    window.location.href = prefix + 'login.html';
}
