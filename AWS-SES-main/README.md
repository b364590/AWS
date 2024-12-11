目前完成使用python後端實現ses郵件寄發和郵件驗證，規劃將範例程式在修改得更簡潔
需要先: 
pip install python-dotenv
pip install boto3
之後應該就可以run python file了

8/3 針對AWS SES的功能 進行以下功能增加 並修改程式碼之結構
(1) 結構修改 -> 針對程式碼功能部分進行檔案分類 增加維護以及修改之可行性
    I. config.py - 配置文件
   II.ses_identity.py - SES 身份管理
  III.ses_mail_sender.py - 郵件發送功能
   IV.ses_template.py - 郵件模板管理
    V.message_queue.py- 流水線排隊式的訊息收發
   VI.main.py - 主程序和演示功能
  VII.email_template.py - 用於訊息模板設計

(2) 針對傳送訊息 進行流程建構 因為此功能主要是聚焦在MODEL訓練過程中提供輔助訊息給使用者 所以我們可能會在同一個時段需要傳送多個人或者會有排隊依序傳送的事情 因為訊息是已經建構好的 所以我們可以專注於如何做成一個流水線傳遞式訊息收發系統 所以我們添加一個Message_queue的python檔案 用於對訊息進行對列控制
   I.導入了 MessageQueue。
  II.創建了 MessageQueue 實例。
 III.將原來直接發送郵件的部分改為使用 message_queue.add_message() 添加消息到隊列。
  IV.對於模板郵件，添加了 message_queue.add_templated_message() 方法（這個方法需要在 MessageQueue 類中實現）。
   V.在發送郵件之前調用 message_queue.start_processing()，開始處理隊列。
  VI.在所有郵件添加到隊列後，調用 message_queue.wait_for_completion() 等待所有郵件發送完成（這個方法也需要在 MessageQueue 類現）
 VII.最後調用 message_queue.stop_processing() 停止隊列處理。

移除了直接使用 SMTP 發送郵件的部分，因為現在所有的郵件發送都通過消息隊列系統處理。

先前均皓的版本我存在Reference.txt中

8/3 針對web註冊時進行驗證與彥君合作後成功達成此功能

8/3 針對後端提供Model progress的api : project_get 進行功能增加
(1) 從後端回傳模型之狀態後 依據status進行分流 並傳送不同的email_template 
(2) 改進message_queue 容納多種status 所造成的多輸入多輸出之影響 進行有效排隊 
