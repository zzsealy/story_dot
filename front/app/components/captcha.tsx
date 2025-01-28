import React, { useEffect, useState } from 'react';
import axios from 'axios'
import Image from 'next/image';


const Captcha = () => {
    const getCaptchaUrl = `${process.env.NEXT_PUBLIC_API_URL}/api/user/get_captcha`
    const validateCaptchaUrl = `${process.env.NEXT_PUBLIC_API_URL}/api/user/validate_captcha`
    const [captchaImage, setCaptchaImage] = useState('');
    const [captchaKey, setCaptchaKey] = useState('')
    const [userInput, setUserInput] = useState('');

    useEffect(() => {
        axios.get(getCaptchaUrl)
          .then((res) => {
            const status_code = res.data.status_code
            if(status_code === 200){
                setCaptchaImage(res.data.captcha_url)
                setCaptchaKey(res.data.captcha_key)
            } else {
                console.log('发生错误')
            }
          })
    })

    const validateCaptcha = () => {
        axios.post(validateCaptchaUrl, {'captcha_key': captchaKey, 'ver_code': {userInput}})
    }

    return (
        <div>
            <Image src={captchaImage} alt="验证码" />
            <input type='text' placeholder='输入验证码' value={userInput} onChange={(e) => setUserInput(e.target.value)}/>
            <button onClick={validateCaptcha}>提交</button>
        </div>
    )

    }