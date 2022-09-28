import win32com.client
olx = win32com.client.gencache.EnsureDispatch("outlook.application")
mapi = olx.GetNamespace("MAPI")
home_folder = mapi.Folders['mine'].Folders['Inbox'].Folders['0_trash_sifter']

CONSTS = {'SMTP_ADDRESS':"http://schemas.microsoft.com/mapi/proptag/0x39FE001E", \
    'ADDRESS_TYPE':"http://schemas.microsoft.com/mapi/proptag/0x39050003"}

with open(r'path\hoobadooba.txt','w') as f:
    for j in home_folder.Items:
        ignore_var = f.write('====NEW-ITEM====\n')
        try:
            sender = j.Sender
            if sender.Type=='EX':
                ignore_var = f.write('From: {}\n'.format(j.Sender.PropertyAccessor.GetProperty(CONSTS['SMTP_ADDRESS'])))
            elif sender.Type=='SMTP':
                ignore_var = f.write('From: {}\n'.format(j.SenderEmailAddress))
        except Exception as e:
            ignore_var = f.write('From: NO_CLUE_MAN\nERROR!! ERROR!!\n===============\n{}\n===============\n\n'.format(e))
        to_list = []
        cc_list = []
        try:
            for i in j.Recipients:
                if i.Type==1:
                    to_list.append(i.PropertyAccessor.GetProperty(CONSTS['SMTP_ADDRESS']))
                elif i.Type==2:
                    cc_list.append(i.PropertyAccessor.GetProperty(CONSTS['SMTP_ADDRESS']))
            ignore_var = f.write('To: {}\n'.format('; '.join(to_list)))
            ignore_var = f.write('CC: {}\n'.format('; '.join(cc_list)))
        except Exception as e:
            ignore_var = f.write('To: NO_CLUE_MAN\nCC: NO_CLUE_MAN\nERROR!! ERROR!!\n===============\n{}\n===============\n\n'.format(e))
        try:
            ignore_var = f.write('Sent: {}\n'.format(j.SentOn.strftime("%Y-%m-%d %H:%M:%S")))
        except Exception as e:
            ignore_var = f.write('Sent: NO_CLUE_MAN\nERROR!! ERROR!!\n===============\n{}\n===============\n\n'.format(e))
        try:
            ignore_var = f.write('Recd: {}\n'.format(j.ReceivedTime.strftime("%Y-%m-%d %H:%M:%S")))
        except Exception as e:
            ignore_var = f.write('Recd: NO_CLUE_MAN\nERROR!! ERROR!!\n===============\n{}\n===============\n\n'.format(e))
        try:
            ignore_var = f.write('Subject: {}\n'.format(j.Subject))
        except Exception as e:
            ignore_var = f.write('Subject: NO_CLUE_MAN\nERROR!! ERROR!!\n===============\n{}\n===============\n\n'.format(e))
        try:
            ignore_var = f.write('{}\n'.format(j.Body))
        except Exception as e:
            ignore_var = f.write('NO_CLUE_MAN\nERROR!! ERROR!!\n===============\n{}\n===============\n\n'.format(e))
