const LoginPage = {
    template: `
    <div class="login-wrapper">
        <div class="login-particles">
            <div v-for="i in 30" :key="i" class="login-particle" :style="particleStyle(i)"></div>
        </div>

        <div class="login-card-container">
            <div class="login-card">
                <div class="login-shine"></div>
                <div class="login-card-inner">
                    <div class="login-icon-wrap">
                        <div class="login-icon-ring"></div>
                        <span class="login-icon">🍜</span>
                    </div>
                    <div class="login-system-name">细粒度情感分析系统</div>
                    <div class="login-system-desc">基于 BERT · 20 维度智能分析 · 餐饮评论</div>

                    <el-form :model="form" :rules="rules" ref="formRef" @keyup.enter="handleLogin" class="login-form">
                        <el-form-item prop="username">
                            <el-input
                                v-model="form.username"
                                placeholder="请输入用户名"
                                size="large"
                                clearable
                                class="login-input"
                            >
                                <template #prefix>
                                    <span class="login-input-icon">👤</span>
                                </template>
                            </el-input>
                        </el-form-item>
                        <el-form-item prop="password">
                            <el-input
                                v-model="form.password"
                                type="password"
                                placeholder="请输入密码"
                                size="large"
                                show-password
                                clearable
                                class="login-input"
                            >
                                <template #prefix>
                                    <span class="login-input-icon">🔒</span>
                                </template>
                            </el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-button
                                type="primary"
                                size="large"
                                class="login-btn"
                                :loading="loading"
                                @click="handleLogin"
                                :disabled="loading"
                            >
                                <span v-if="!loading">登 录 系 统</span>
                                <span v-else>验 证 中...</span>
                            </el-button>
                        </el-form-item>
                    </el-form>

                    <div v-if="error" class="login-error">
                        <el-alert :title="error" type="error" show-icon :closable="false" effect="dark" />
                    </div>
                </div>
            </div>
        </div>
    </div>`,
    setup() {
        const form = Vue.reactive({ username: '', password: '' });
        const loading = Vue.ref(false);
        const error = Vue.ref('');
        const formRef = Vue.ref(null);
        const router = VueRouter.useRouter();

        const rules = {
            username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
            password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
        };

        const handleLogin = async () => {
            const valid = await formRef.value.validate().catch(() => false);
            if (!valid) return;
            loading.value = true;
            error.value = '';
            try {
                const res = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(form),
                });
                const data = await res.json();
                if (res.ok && data.success) {
                    localStorage.setItem('sentiment_token', data.token);
                    localStorage.setItem('sentiment_user', 'admin');
                    router.push('/');
                } else {
                    error.value = data.detail || '登录失败';
                }
            } catch (e) {
                error.value = '网络错误，请稍后重试';
            } finally {
                loading.value = false;
            }
        };

        const particleStyle = (i) => {
            const size = 4 + Math.random() * 10;
            const left = Math.random() * 100;
            const delay = Math.random() * 8;
            const duration = 8 + Math.random() * 15;
            return {
                width: size + 'px',
                height: size + 'px',
                left: left + '%',
                animationDelay: delay + 's',
                animationDuration: duration + 's',
                opacity: 0.15 + Math.random() * 0.35,
            };
        };

        return { form, loading, error, formRef, rules, handleLogin, particleStyle };
    },
};
