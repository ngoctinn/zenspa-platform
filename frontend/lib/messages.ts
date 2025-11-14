// Messages cho tính năng Auth - ZenSpa
// Chuỗi lỗi, nhãn, thông báo để tránh hardcode và hỗ trợ i18n sau này

export const authMessages = {
  // Labels cho form
  labels: {
    email: "Email",
    password: "Mật khẩu",
    confirmPassword: "Xác nhận mật khẩu",
    fullName: "Họ và tên",
    newPassword: "Mật khẩu mới",
    confirmNewPassword: "Xác nhận mật khẩu mới",
    rememberMe: "Ghi nhớ đăng nhập",
    forgotPassword: "Quên mật khẩu?",
    signIn: "Đăng nhập",
    signUp: "Đăng ký",
    resetPassword: "Đặt lại mật khẩu",
    sendResetEmail: "Gửi email đặt lại",
    setNewPassword: "Đặt mật khẩu mới",
    backToSignIn: "Quay lại đăng nhập",
    goHome: "Quay về trang chủ",
  },

  // Validation errors
  validation: {
    emailRequired: "Email là bắt buộc",
    emailInvalid: "Email không hợp lệ",
    passwordRequired: "Mật khẩu là bắt buộc",
    passwordTooShort: "Mật khẩu phải có ít nhất 8 ký tự",
    passwordTooLong: "Mật khẩu không được quá 30 ký tự",
    confirmPasswordRequired: "Xác nhận mật khẩu là bắt buộc",
    passwordsNotMatch: "Mật khẩu xác nhận không khớp",
    fullNameRequired: "Họ và tên là bắt buộc",
    fullNameTooShort: "Họ và tên phải có ít nhất 2 ký tự",
  },

  // Success messages
  success: {
    signUpSuccess:
      "Bạn đã đăng ký thành công! Vui lòng kiểm tra email để xác minh tài khoản của bạn.",
    signInSuccess: "Đăng nhập thành công!",
    resetEmailSent:
      "Email đặt lại mật khẩu đã được gửi. Vui lòng kiểm tra hộp thư.",
    passwordResetSuccess: "Mật khẩu đã được đặt lại thành công!",
  },

  // Error messages (từ Supabase hoặc general)
  errors: {
    signUpFailed: "Đăng ký thất bại. Vui lòng thử lại.",
    signInFailed: "Đăng nhập thất bại. Kiểm tra email và mật khẩu.",
    emailAlreadyExists: "Email này đã được sử dụng.",
    invalidCredentials: "Thông tin đăng nhập không hợp lệ.",
    userNotConfirmed: "Tài khoản chưa được xác minh. Vui lòng kiểm tra email.",
    resetFailed: "Gửi email đặt lại thất bại. Vui lòng thử lại.",
    resetPasswordFailed: "Đặt lại mật khẩu thất bại. Vui lòng thử lại.",
    networkError: "Lỗi mạng. Vui lòng kiểm tra kết nối.",
    unknownError: "Đã xảy ra lỗi không xác định. Vui lòng thử lại.",
  },

  // Thông báo khác
  info: {
    checkEmail: "Vui lòng kiểm tra email để xác minh tài khoản.",
    timeRemaining: "Thời gian còn lại",
  },
} as const;
