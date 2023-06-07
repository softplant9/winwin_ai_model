import streamlit as st
import openai as op
       
op.api_key = st.secrets["OPENAI_API_KEY"]

st.title("GOLF AI engineered by TINO5")
st.write("")

tab1, tab2 = st.tabs([" ", "Golf Fitting"])

with tab1:
    with st.form(key="form_key_tab1"):
       prompt_input = st.text_input(label='Enter your prompt', placeholder='Enter your prompt')
       selected_size = st.selectbox("Size", ["256x256", "512x512", "1024x1024"])
       submit_button = st.form_submit_button(label='Submit')
       
       if submit_button and prompt_input:
            gpt_prompt = [{
                "role": "system",
                "content": "Imagine the detail appearance of the input. Response it around 20 words."
            }]

            gpt_prompt.append({
                "role": "user",
                "content": prompt_input
            })

            with st.spinner(text='Generating prompt...'):
                gpt_response = op.ChatCompletion.create(
                    model = "gpt-3.5-turbo",
                    messages=gpt_prompt
                )

            prompt_from_gpt = gpt_response.choices[0]["message"]["content"]

            st.write(prompt_from_gpt)
            st.write("")

            with st.spinner(text='Generating image...'):
                dalle_response = op.Image.create(
                    prompt = prompt_from_gpt, 
                    size = selected_size
                )

            st.image(dalle_response["data"][0]["url"])


with tab2:
    with st.form(key="form_key_tab2"):
        
        st.subheader('Tell me about you')
        
        club_no = st.selectbox('Club No.', ('Driver', 'Wood', 'Iron', 'Wedge'))
        fitting_why = st.selectbox('What are you fitting now?', ('For Distance', 'For Draw', 'For Fade'))
        brands = st.multiselect('What are your favorite brand?', ['Fujikura Ventus', 'Mitsubishi Tensei', 'Graphite Design Tour AD'], default=['Fujikura Ventus', 'Mitsubishi Tensei'])
        
        st.subheader('Enter average trackman data')
        club_speed = st.text_input(label='Club speed (mph)', value="100")
        ball_speed = st.text_input(label='Ball speed (mph)', value="150")
        smash_factor = st.text_input(label='Smash Factor', value="1.5")
        attack_angle = st.text_input(label='Attack angle (degree)', value="-1.3")
        launch_angle = st.text_input(label='Launch Angle (degree)', value="10.9")
        spin_rate = st.text_input(label='Spin rate (rpm)', value="2686")
        max_height = st.text_input(label='Max height (yards)', value="32")
        carry = st.text_input(label='Carry (yards)', value="276" )
        
        submit_button = st.form_submit_button(label='Submit')
        
        if (submit_button and club_speed and ball_speed and smash_factor and attack_angle and launch_angle and spin_rate and max_height and carry) == False:
            st.write("Please fill all the fields")
        
        else:
            if fitting_why == 'For Distance':
                content = "저의 골프 " + club_no + " 스윙을 분석해서 거리를 더 늘리기 위해서 어떤 스펙의 샤프트를 사용해야되는지 알려줬으면 좋겠습니다." + "\n"
            elif fitting_why == 'For Draw':
                content = "저의 골프 " + club_no + " 스윙을 분석해서 Draw 구질을 만들기 위해서 어떤 스펙의 샤프트를 사용해야되는지 알려줬으면 좋겠습니다." + "\n"
            else:
                content = "저의 골프 " + club_no + " 스윙을 분석해서 Fade 구질을 만들기 위해서 어떤 스펙의 샤프트를 사용해야되는지 알려줬으면 좋겠습니다." + "\n"
                
            content = content + "그러기 위해서는 트랙맨에서 나오는 Club speed, ball speed, smash factor, attack_angle, launch angle, spin rate, max height, carry 등의 수치들을 이해해야 합니다." + "\n"
            content = content + "이 수치들을 이해하고 분석해서 나에게 가장 적합한 " + club_no + " 샤프트 스펙을 Flex(즉, Stiffness), Weight, Torque 기준으로 알려주되, "
            content = content + "샤프트 브랜드는 " + ", ".join(brands) + " 로 추천해주면 좋겠습니다." + "\n"
            
            #st.write(content)
            
            gpt_prompt = [{
                "role": "user",
                "content": content
            }]
            
            content = content + "이제 저의 trackman 스윙 데이터와 여러 샤프트 모델의 스펙을 공유해 드리겠습니다. 부가적인 설명은 제외하고 추천 샤프트의 모델명 2개만 추려서 대답해주세요."
            
            content = content + "trackman data 는 아래와 같다." + "\n"
            content = content + "- Club Speed: " + club_speed + " mph" + "\n"
            content = content + "- Attack angle: " + attack_angle +"-1.3 degree" + "\n"
            content = content + "- Ball speed: " + ball_speed + " mph" + "\n"
            content = content + "- Smash Factor: " + smash_factor + "\n"
            content = content + "- Launch Angle: " + launch_angle + " degree" + "\n"
            content = content + "- Spin rate: " + spin_rate + " rpm" + "\n"
            content = content + "- Max height: " + max_height + " yards" + "\n"
            content = content + "- Carry: " + carry + " yards" + "\n"
            
            gpt_prompt.append({
                "role": "user",
                "content": content
            })
            
            with st.spinner(text='Analysing swing data...'):
                gpt_response = op.ChatCompletion.create(
                    model = "gpt-3.5-turbo",
                    messages=gpt_prompt
                )

            prompt_from_gpt = gpt_response.choices[0]["message"]["content"]
                
            st.write(prompt_from_gpt)
            st.write("")
            
            if False:
                content = "아래 샤프트들 중에서 추천해줬으면 한다." + "\n"
                content = content + "Ventus Blue 5 Flex R2 모델 : Flex R2, Length 46, Weight 58, Torque 4" + "\n"
                content = content + "Ventus Blue 5 Flex R 모델 : Flex R, Length 46, Weight 58.5, Torque 3.7" + "\n"
                content = content + "Ventus Blue 5 Flex S 모델 : Flex S, Length 46, Weight 59, Torque 3.3" + "\n"
                content = content + "Ventus Blue 6 Flex R 모델 : Flex R, Length 46, Weight 65, Torque 3.5" + "\n"
                content = content + "Ventus Blue 6 Flex S 모델 : Flex S, Length 46, Weight 65, Torque 3.1" + "\n"
                content = content + "Ventus Blue 6 Flex X 모델 : Flex x, Length 46, Weight 65, Torque 3.1" + "\n"
                content = content + "Ventus Blue 6 Flex TX 모델 : Flex tx, Length 46, Weight 68.5, Torque 3.1" + "\n"
                content = content + "Ventus Blue 7 Flex S 모델 : Flex S, Length 46, Weight 76, Torque 3" + "\n"
                content = content + "Ventus Blue 7 Flex X 모델 : Flex X, Length 46, Weight 77.5, Torque 2.9" + "\n"
                content = content + "Ventus Blue 7 Flex TX 모델 : Flex tx, Length 46, Weight 79.5, Torque 2.9" + "\n"
                content = content + "Ventus Blue 8 Flex S 모델 : Flex s, Length 46, Weight 86, Torque 3" + "\n"
                content = content + "Ventus Blue 8 Flex X 모델 : Flex X, Length 46, Weight 86, Torque 2.8" + "\n"
                content = content + "Ventus Blue 8 Flex TX 모델 : Flex tx, Length 46, Weight 84.5, Torque 2.9" + "\n"
                content = content + "Ventus Blue 9 Flex X 모델 : Flex X, Length 46, Weight 94.5, Torque 2.8" + "\n"
                content = content + "Ventus Blue 9 Flex TX 모델 : Flex TX, Length 46, Weight 94.5, Torque 2.9" + "\n"
                content = content + "Ventus Black 5 Flex X 모델 : Flex X, Length 46, Weight 58, Torque 3.3" + "\n"
                content = content + "Ventus Black 6 Flex S 모델 : Flex S, Length 46, Weight 64, Torque 3.4" + "\n"
                content = content + "Ventus Black 6 Flex X 모델 : Flex X, Length 46, Weight 65, Torque 3.1" + "\n"
                content = content + "Ventus Black 6 Flex TX 모델 : Flex tx, Length 46, Weight 65, Torque 3.1" + "\n"
                content = content + "Ventus Black 7 Flex S 모델 : Flex S, Length 46, Weight 76, Torque 3" + "\n"
                content = content + "Ventus Black 7 Flex X 모델 : Flex X, Length 46, Weight 77.5, Torque 2.9" + "\n"
                content = content + "Ventus Black 7 Flex TX 모델 : Flex tx, Length 46, Weight 79.5, Torque 2.9" + "\n"
                content = content + "Ventus Black 8 Flex S 모델 : Flex s, Length 46, Weight 86, Torque 3" + "\n"
                content = content + "Ventus Black 8 Flex X 모델 : Flex X, Length 46, Weight 86, Torque 2.8" + "\n"
                content = content + "Ventus Black 8 Flex TX 모델 : Flex tx, Length 46, Weight 84.5, Torque 2.9" + "\n"
                content = content + "Ventus Black 9 Flex X 모델 : Flex X, Length 46, Weight 94.5, Torque 2.8" + "\n"
                content = content + "Ventus Black 9 Flex TX 모델 : Flex TX, Length 46, Weight 94.5, Torque 2.9" + "\n"
                
                if False:
                    content = content + "Ventus Red 5 Flex R2 모델 : Flex R2, Length 46, Weight 58, Torque 4" + "\n"
                    content = content + "Ventus Red 5 Flex R 모델 : Flex R, Length 46, Weight 58.5, Torque 3.7" + "\n"
                    content = content + "Ventus Red 5 Flex S 모델 : Flex S, Length 46, Weight 59, Torque 3.3" + "\n"
                    content = content + "Ventus Red 6 Flex R 모델 : Flex R, Length 46, Weight 65, Torque 3.5" + "\n"
                    content = content + "Ventus Red 6 Flex S 모델 : Flex S, Length 46, Weight 65, Torque 3.1" + "\n"
                    content = content + "Ventus Red 6 Flex X 모델 : Flex x, Length 46, Weight 65, Torque 3.1" + "\n"
                    content = content + "Ventus Red 6 Flex TX 모델 : Flex tx, Length 46, Weight 68.5, Torque 3.1" + "\n"
                    content = content + "Ventus Red 7 Flex S 모델 : Flex S, Length 46, Weight 76, Torque 3" + "\n"
                    content = content + "Ventus Red 7 Flex X 모델 : Flex X, Length 46, Weight 77.5, Torque 2.9" + "\n"
                    content = content + "Ventus Red 7 Flex TX 모델 : Flex tx, Length 46, Weight 79.5, Torque 2.9" + "\n"
                    content = content + "Ventus Red 8 Flex S 모델 : Flex s, Length 46, Weight 86, Torque 3" + "\n"
                    content = content + "Ventus Red 8 Flex X 모델 : Flex X, Length 46, Weight 86, Torque 2.8" + "\n"
                    content = content + "Ventus Red 8 Flex TX 모델 : Flex tx, Length 46, Weight 84.5, Torque 2.9" + "\n"
                    content = content + "Ventus Red 9 Flex X 모델 : Flex X, Length 46, Weight 94.5, Torque 2.8" + "\n"
                    content = content + "Ventus Red 9 Flex TX 모델 : Flex TX, Length 46, Weight 94.5, Torque 2.9" + "\n"
                
                if False:
                    content = content + "TENSEI™ AV Blue 55 모델 : Flex R, Length 46, Weight 55, Torque 5.2" + "\n"
                    content = content + "TENSEI™ AV Blue 55 모델 : Flex S, Length 46, Weight 57, Torque 5.2" + "\n"
                    content = content + "TENSEI™ AV Blue 55 모델 : Flex X, Length 46, Weight 59, Torque 5.2" + "\n"
                    content = content + "TENSEI™ AV Blue 55 모델 : Flex TX, Length 46, Weight 61, Torque 5.2" + "\n"
                    content = content + "TENSEI™ AV Blue 65 모델 : Flex R, Length 46, Weight 65, Torque 4.4" + "\n"
                    content = content + "TENSEI™ AV Blue 65 모델 : Flex S, Length 46, Weight 67, Torque 4.4" + "\n"
                    content = content + "TENSEI™ AV Blue 65 모델 : Flex X, Length 46, Weight 69, Torque 4.4" + "\n"
                    content = content + "TENSEI™ AV Blue 65 모델 : Flex TX, Length 46, Weight 71, Torque 4.4" + "\n"
                    content = content + "TENSEI™ AV Blue 75 모델 : Flex S, Length 46, Weight 77, Torque 4.2" + "\n"
                    content = content + "TENSEI™ AV Blue 75 모델 : Flex X, Length 46, Weight 79, Torque 4.2" + "\n"
                    content = content + "TENSEI™ AV Blue 75 모델 : Flex TX, Length 46, Weight 81, Torque 4.2" + "\n"
                    content = content + "TENSEI™ AV Blue 85 모델 : Flex S, Length 46, Weight 87, Torque 3.9" + "\n"
                    content = content + "TENSEI™ AV Blue 85 모델 : Flex X, Length 46, Weight 89, Torque 3.9" + "\n"
                    content = content + "TENSEI™ AV Blue 85 모델 : Flex TX, Length 46, Weight 91, Torque 3.9" + "\n"
                    content = content + "TENSEI™ AV Blue 95 모델 : Flex S, Length 46, Weight 97, Torque 3.8" + "\n"
                    content = content + "TENSEI™ AV Blue 95 모델 : Flex X, Length 46, Weight 99, Torque 3.8" + "\n"
                    content = content + "TENSEI™ AV Blue 95 모델 : Flex TX, Length 46, Weight 101, Torque 3.8" + "\n"
                
                content = content + "TENSEI™ 1K Pro White 50 R 모델: Flex R, weight 54, torque 4.6" + "\n"
                content = content + "TENSEI™ 1K Pro White 50 S 모델: Flex S, weight 56, torque 4.5" + "\n"
                content = content + "TENSEI™ 1K Pro White 50 X 모델: Flex X, weight 59, torque 4.4" + "\n"
                content = content + "TENSEI™ 1K Pro White 50 TX 모델: Flex TX, weight 61, torque 4.4" + "\n"
                content = content + "TENSEI™ 1K Pro White 60 R 모델: Flex R, weight 60, torque 3.8" + "\n"
                content = content + "TENSEI™ 1K Pro White 60 S 모델: Flex S, weight 62, torque 3.8" + "\n"
                content = content + "TENSEI™ 1K Pro White 60 X 모델: Flex X, weight 65, torque 3.8" + "\n"
                content = content + "TENSEI™ 1K Pro White 60 TX 모델: Flex TX, weight 67, torque 3.8" + "\n"
                content = content + "TENSEI™ 1K Pro White 70 S 모델: Flex S, weight 71, torque 3.4" + "\n"
                content = content + "TENSEI™ 1K Pro White 70 X 모델: Flex X, weight 75, torque 3.4" + "\n"
                content = content + "TENSEI™ 1K Pro White 70 TX 모델: Flex TX, weight 79, torque 3.4" + "\n"
                content = content + "TENSEI™ 1K Pro White 80 S 모델: Flex S, weight 81, torque 3.2" + "\n"
                content = content + "TENSEI™ 1K Pro White 80 X 모델: Flex X, weight 85, torque 3.2" + "\n"
                content = content + "TENSEI™ 1K Pro White 80 TX 모델: Flex TX, weight 89, torque 3.2" + "\n"
                
                content = content + "TENSEI™ 1K Pro Orange 50 R 모델: Flex R, weight 54, torque 3.9" + "\n"
                content = content + "TENSEI™ 1K Pro Orange 50 S 모델: Flex S, weight 56, torque 3.9" + "\n"
                content = content + "TENSEI™ 1K Pro Orange 50 X 모델: Flex X, weight 58, torque 3.8" + "\n"
                content = content + "TENSEI™ 1K Pro Orange 50 TX 모델: Flex TX, weight 59, torque 3.8" + "\n"
                content = content + "TENSEI™ 1K Pro Orange 60 R 모델: Flex R, weight 66, torque 3" + "\n"
                content = content + "TENSEI™ 1K Pro Orange 60 S 모델: Flex S, weight 68, torque 3" + "\n"
                content = content + "TENSEI™ 1K Pro Orange 60 X 모델: Flex X, weight 70, torque 3" + "\n"
                content = content + "TENSEI™ 1K Pro Orange 60 TX 모델: Flex TX, weight 71, torque 3" + "\n"
                content = content + "TENSEI™ 1K Pro Orange 70 S 모델: Flex S, weight 77, torque 2.7" + "\n"
                content = content + "TENSEI™ 1K Pro Orange 70 X 모델: Flex X, weight 79, torque 2.7" + "\n"
                content = content + "TENSEI™ 1K Pro Orange 70 TX 모델: Flex TX, weight 81, torque 2.7" + "\n"
                content = content + "TENSEI™ 1K Pro Orange 80 S 모델: Flex S, weight 83, torque 2.5" + "\n"
                content = content + "TENSEI™ 1K Pro Orange 80 X 모델: Flex X, weight 85, torque 2.5" + "\n"
                content = content + "TENSEI™ 1K Pro Orange 80 TX 모델: Flex TX, weight 87, torque 2.5" + "\n"
                
                if False:
                    content = content + "TENSEI™ 1K Black 65 모델: Flex S, weight 67, torque 3.6" + "\n"
                    content = content + "TENSEI™ 1K Black 65 모델: Flex X, weight 68, torque 3.5" + "\n"
                    content = content + "TENSEI™ 1K Black 65 모델: Flex TX, weight 69, torque 3.5" + "\n"
                    content = content + "TENSEI™ 1K Black 75 모델: Flex S, weight 76, torque 3.6" + "\n"
                    content = content + "TENSEI™ 1K Black 75 모델: Flex X, weight 78, torque 3.5" + "\n"
                    content = content + "TENSEI™ 1K Black 75 모델: Flex TX, weight 79, torque 3" + "\n"
                    content = content + "TENSEI™ 1K Black 85 모델: Flex S, weight 89, torque 3.2" + "\n"
                    content = content + "TENSEI™ 1K Black 85 모델: Flex X, weight 90, torque 3.2" + "\n"
                    content = content + "TENSEI™ 1K Black 85 모델: Flex TX, weight 90, torque 2.8" + "\n"
                    
                content = content + "TENSEI 1K Pro Blue 50 R 모델: Flex R, weight 52, torque 4.9" + "\n"
                content = content + "TENSEI 1K Pro Blue 50 S 모델: Flex S, weight 54, torque 4.9" + "\n"
                content = content + "TENSEI 1K Pro Blue 50 X 모델: Flex X, weight 56, torque 4.9" + "\n"
                content = content + "TENSEI 1K Pro Blue 50 TX 모델: Flex TX, weight 57, torque 4.9" + "\n"
                content = content + "TENSEI 1K Pro Blue 60 R 모델: Flex R, weight 64, torque 3.8" + "\n"
                content = content + "TENSEI 1K Pro Blue 60 S 모델: Flex S, weight 66, torque 3.8" + "\n"
                content = content + "TENSEI 1K Pro Blue 60 X 모델: Flex X, weight 68, torque 3.8" + "\n"
                content = content + "TENSEI 1K Pro Blue 60 TX 모델: Flex TX, weight 69, torque 3.8" + "\n"
                content = content + "TENSEI 1K Pro Blue 70 S 모델: Flex S, weight 75, torque 3.4" + "\n"
                content = content + "TENSEI 1K Pro Blue 70 X 모델: Flex X, weight 77, torque 3.4" + "\n"
                content = content + "TENSEI 1K Pro Blue 70 TX 모델: Flex TX, weight 79, torque 3.4" + "\n"
                content = content + "TENSEI 1K Pro Blue 80 S 모델: Flex S, weight 82, torque 3.2" + "\n"
                content = content + "TENSEI 1K Pro Blue 80 X 모델: Flex X, weight 84, torque 3.2" + "\n"
                content = content + "TENSEI 1K Pro Blue 80 TX 모델: Flex TX, weight 86, torque 3.2" + "\n"
                                    
                gpt_prompt_2 = [{
                    "role": "user",
                    "content": content
                }]
                
                with st.spinner(text='Generating prompt 2...'):
                    gpt_response_2 = op.ChatCompletion.create(
                        model = "gpt-3.5-turbo",
                        messages=gpt_prompt_2
                    )

                prompt_from_gpt_2 = gpt_response_2.choices[0]["message"]["content"]
                
                st.write(prompt_from_gpt_2)
                st.write("")