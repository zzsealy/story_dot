
import React, { useEffect, useState } from 'react';
import axios from 'axios'

interface CaptchaDisplayProps {
    onCaptchaChange: (captchaKey: string) => void;
}

const CaptchaDisplay: React.FC<CaptchaDisplayProps> = ({onCaptchaChange}) => {
    const [captchaImage, setCaptchaImage] = useState('');

    const fetchCaptcha = () =>{
        const getCaptchaUrl = `${process.env.NEXT_PUBLIC_API_URL}/api/user/get_captcha`
        axios.get(getCaptchaUrl)
          .then((res) => {
            const status_code = res.data.status_code
            if(status_code === 200){
                debugger;
                const captchaUrl = `${process.env.NEXT_PUBLIC_API_URL}${res.data.captcha_url}`
                setCaptchaImage(captchaUrl)
                onCaptchaChange(res.data.captcha_key) // 调用回调函数来通知父组件
            } else {
                console.log('发生错误')
            }
          })
    }
    useEffect(() => {
        // 任何作用域外的变量，都被视为潜在的依赖项
        fetchCaptcha();
    }, []);

    const handleCaptchaClick = () => {
        fetchCaptcha(); // **添加：点击刷新验证码**
    };
    

    return (

      <div className='space-y-2'>
        { captchaImage && <img width={100} height={20} src={captchaImage} alt="验证码" onClick={handleCaptchaClick}/> }
        {/* <Label htmlFor="ver_code">验证码</Label> */}
      </div>
    )

    }

export default CaptchaDisplay