import React, { useEffect, useState } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import axios from 'axios'
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

interface FormValues {
    ver_code: string
}

const CaptchaForm: React.FC = () => {
    const { register, handleSubmit, formState: { errors } } = useForm<FormValues>();
    const validateCaptchaUrl = `${process.env.NEXT_PUBLIC_API_URL}/api/user/validate_captcha`
    const [captchaImage, setCaptchaImage] = useState('');
    const [captchaKey, setCaptchaKey] = useState('')
    const [clickCaptchaTime, setClickCaptchaTime] = useState(0)

    useEffect(() => {
        // 任何作用域外的变量，都被视为潜在的依赖项
        const getCaptchaUrl = `${process.env.NEXT_PUBLIC_API_URL}/api/user/get_captcha`
        axios.get(getCaptchaUrl)
          .then((res) => {
            const status_code = res.data.status_code
            if(status_code === 200){
                setCaptchaImage(`${process.env.NEXT_PUBLIC_API_URL}${res.data.captcha_url}`)
                setCaptchaKey(res.data.captcha_key)
            } else {
                console.log('发生错误')
            }
          })
    }, [clickCaptchaTime]);

    const onSubmit: SubmitHandler<FormValues> = (values) => {

        axios.post(validateCaptchaUrl, {'captcha_key': captchaKey, 'ver_code': values.ver_code})
          .then((res) => {
            const status_code = res.data.status_code
            if(status_code===200){
                console.log(res.data)
            }
          })
    }

    const handleCaptchaClick = () => {
        setClickCaptchaTime(clickCaptchaTime + 1)
    }
    

    return (

    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className='space-y-2'>
        { captchaImage && <img width={100} height={20} src={captchaImage} alt="验证码" onClick={handleCaptchaClick}/> }
        {/* <Label htmlFor="ver_code">验证码</Label> */}
        <Input
          id="ver_code"
          {...register('ver_code', { required: 'Username is required' })}
        />

        {errors.ver_code && <span className="text-red-500">{errors.ver_code.message}</span>}
      </div>

      <Button type="submit" className='bg-green-400'>提交</Button>
    </form>
        // <div className='space-y-2'>
        //     { captchaImage && <img width={100} height={20} src={captchaImage} alt="验证码" /> }
        //     <input type='text' placeholder='输入验证码' value={userInput} onChange={(e) => setUserInput(e.target.value)}/>
        //     <div>
        //         <Button  onClick={validateCaptcha}>提交</Button>
        //     </div>        
        // </div>
    )

    }

export default CaptchaForm