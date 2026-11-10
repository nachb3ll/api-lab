# API lab results

## Part 0

- Step 0.1, the number of pizza names: 18
- Step 0.3, status code of the request without a token: 401
- Step 0.4, the name of your pizza: A Dead Bolognese
- Step 0.12, results of the three runs without a session: run 1 passed; runs 2 and 3 failed at login with 401 
- Step 0.16, blocks of "how many of the three tools are excluded": 0, 1, 2 และ 3 

## Defect report

- Title: การ exclude เครื่องมือทั้งหมดทำให้เกิด empty 500 response
- Request: `POST /api/pizza`, ใช้ token ของผู้ใช้ทดสอบ และส่ง {"excludedTools":["Knife","Pizza cutter","Scissors"]} `{"excludedTools":["Knife","Pizza cutter","Scissors"]}`.
- Expected result: Status 400 และ JSON error ที่แสดงข้อความไม่มีพิซซ่าที่ตรงเงื่อนไข
- Actual result: Status 500 และ response body ว่าง
- Severity: Medium เนื่องจาก request มีรูปแบบถูกต้องแต่สามารถทำให้ server เกิด error ได้ และ response ที่ว่างไม่ให้ข้อมูลที่เป็นประโยชน์แก่ API client อย่างไรก็ตาม defect นี้ไม่ได้ทำให้ข้อมูล rating ที่บันทึกไว้เปลี่ยนแปลง

## Part A

- Step A4, other user's read, update, and delete status codes: 404, 400 และ 400 ตามลำดับ การอ่าน rating อีกครั้งโดยเจ้าของได้ status 200 ทุกครั้ง และพบว่า rating เดิมไม่เปลี่ยนแปลง ดังนั้นทั้ง 3 requests ของผู้ใช้อื่นถูกปฏิเสธด้วย status 4xx ตามที่โจทย์กำหนด
404, 400, and 400. The owner's follow-up read returned 200 each time and showed the original rating unchanged. All three attempts were refused with 4xx responses, as required by the exercise.

## Part B: Reflection

1. Your tests talk to a real server over the internet. Name two kinds of failure that they can find and
a unit test with stubs cannot. Then give one reason to write unit tests with stubs as well.

Ans API test พบปัญหาการยืนยันตัวตนจริงและการบันทึกข้อมูลจริงได้ ส่วน unit test ที่ใช้ stub ไม่ได้ทดสอบการเชื่อมต่อเหล่านี้ แต่ unit test รันเร็วและช่วยระบุจุดที่ logic ผิดได้ง่าย

2. Why does every test create its own user with a new name, rather than use the public token?
How will you apply the same idea to the shared shop or hotel in Project 2?

Ans แต่ละ test สร้าง user ใหม่เพื่อป้องกันไม่ให้ข้อมูลของ test หนึ่งชนหรือกระทบกับข้อมูลของ test อื่นหรือผู้ใช้งานคนอื่น สำหรับ Project 2 จะใช้แนวคิดเดียวกัน โดยสร้างข้อมูลที่ใช้สำหรับการทดสอบของกลุ่มเอง และลบเฉพาะข้อมูลที่กลุ่มเป็นผู้สร้าง

3. Explain in your own words why the tests send every request through one session. If you did
Step 0.12, describe what happened in your three runs.

Ans การใช้ session ทำให้ cookies ที่ server ส่งกลับมาถูกเก็บไว้ และทำให้ request ต่าง ๆ สามารถเชื่อมต่อกับ server เดิมผ่าน load balancer ได้อย่างต่อเนื่อง หากไม่ใช้ session การทดสอบครั้งที่ 1 ผ่าน แต่ครั้งที่ 2 และ 3 login ไม่สำเร็จและได้ status 401


4. Which block of the excluded tools revealed the defect in Step 0.16? Why is a 500 with an empty
body worse for an app that calls the API than a 400 with a message? Why does the test stay in
the suite as xfail instead of being deleted?

Ans บล็อกที่พบ defect คือกรณีที่ exclude เครื่องมือทั้ง 3 ชนิด ได้แก่ Knife, Pizza cutter และ Scissors การได้ status 500 พร้อม response body ที่ว่างมีปัญหาสำหรับ application ที่เรียก API เพราะ application ไม่ได้รับข้อมูลที่บอกว่าเกิดอะไรขึ้นหรือควรแก้ request อย่างไร ในทางกลับกัน status 400 พร้อม error message จะช่วยให้ client เข้าใจว่า request ไม่สามารถทำได้และทราบสาเหตุ สามารถคง test นี้ไว้เป็น xfail แทนการลบ เพราะต้องการให้ defect ยังคงถูกติดตามอยู่ใน test suite และเมื่อระบบได้รับการแก้ไขแล้ว strict=True จะช่วยแจ้งให้ทราบว่าควรลบ xfail ออก

5. How many tests does base choice coverage need for the model in Step A1, and how many
would all combinations coverage need? Show how you counted.

Ans Base choice ใช้ `1 + (3-1) + (4-1) + (2-1) + (3-1) = 9` tests ส่วน all combinations ใช้ `3 × 4 × 2 × 3 = 72` tests

6. In Step A4, which status codes did you get when the other user read, changed and deleted the
rating? Which codes would you expect? Is the difference a defect? Explain.

Ans ผู้ใช้อื่นที่พยายามอ่าน rating ได้ status 404 แก้ไข rating ได้ status 400 และลบ rating ได้ status 400 โดยสิ่งที่คาดหวัง คือทุก request ของผู้ใช้อื่นต้องถูกปฏิเสธด้วย status 4xx และ rating ต้องไม่ถูกเปลี่ยนแปลง ดังนั้นความแตกต่างระหว่าง 404 และ 400 ไม่ถือเป็น defect ตามเกณฑ์ของโจทย์ เพราะทั้งสองกรณีเป็น status code ในกลุ่ม 4xx และการกระทำถูกปฏิเสธ

7. Create madeup.txt with the line Authorization: token 0000000000000000, a made-up
token of 16 characters, and run the command below. What comes back? Is this a defect, and
what could a stranger do with it on a real system? Only read with this token, and never create or
change anything with it.
curl -H "@madeup.txt" https://quickpizza.grafana.com/api/ratings

Ans ผลลัพธ์นี้ถือเป็น defect ด้าน authorization เพราะบุคคลที่ไม่มี token ที่ถูกต้องสามารถเข้าถึงข้อมูล ratings ได้ หากเป็นระบบจริง บุคคลภายนอกอาจสามารถอ่านข้อมูลที่ไม่ควรเข้าถึงได้ ในการทดสอบนี้ใช้ token ดังกล่าวสำหรับการอ่านข้อมูลเท่านั้น และไม่ได้ใช้เพื่อสร้างหรือเปลี่ยนแปลงข้อมูล

8. Name one thing that an API test checks better than a test through the web pages, and one thing
that only a test through the web pages can check.

Ans API test สามารถตรวจสอบ status code และข้อมูล JSON ที่ server ส่งกลับมาได้โดยตรงและละเอียด ในขณะที่การทดสอบผ่าน web page สามารถตรวจสอบสิ่งที่ผู้ใช้มองเห็นและโต้ตอบด้วยได้ เช่น การแสดงผลของหน้าเว็บและการทำงานของส่วนติดต่อผู้ใช้
้
## Full test run

- `pytest -v`: 32 passed, 1 xfailed.

