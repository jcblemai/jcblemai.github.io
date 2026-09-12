---
title: "How to save you institutional mailbox and calendars"
date: "2022-06-02T15:30:38"
lastmod: "2025-07-21T10:01:39"
draft: false
slug: "how-to-save-you-institutional-mailbox-and-calendars"
wordpress_id: 96
wordpress_type: "post"
wordpress_status: "publish"
wordpress_title: "How to save you institutional mailbox and calendars"
wordpress_url: "https://josephlemaitre.com/2022/06/how-to-save-you-institutional-mailbox-and-calendars/"
author: "josephlemaitre"
categories: ["stuff"]
tags: []
layout: "post"
permalink: "/2022/06/how-to-save-you-institutional-mailbox-and-calendars/"
published: true
render_with_liquid: false
---

How I did it:

37C20BE2-E02F-48F5-91BA-2275086E138E is lmtre.fr

315CFCFE-F902-499E-BD53-259AC0F21BB6 is gmail.com

17199DDE-A3A1-40C7-8FBB-662F004532AF is EPFL.ch

C6245073-FCAB-4DA4-A21C-A54693C7E882 is iCloud

CBB567A4-CD0F-4ED5-A5A0-6DAE30511627 is Unive.it

E42160D9-B9F7-4677-B659-46CA4CAF9158 is unc.edu

Academics moves often, and for example I was affiliated with 3 different institutions in 2021. After some time, it's unusual

I'm writing this up because it took me one full day and it should not have.

## Email

Requirements:

-   be searchable
-   include attachement
-   be complete
-   be somewhat standard if I go back to linux

My PhD institutional mailbox uses 3.95Go of storage and there are

-   9'986 messages in Archive (Thunderbird says 10'245, for some reason)
-   3'053 in Sent (again, 3'055 from Thunderbird)
-   43 messages in Inbox

Which mean I responded to 1/3 of the email ? weird I would expect this ratio to be way lower (I delete spammy emails on the fly).

### what did not work

My email are synced with MacOS Mail.app. In there, you can two finger click, and choose export mailbox in the contextual menu. It's not really a polished feature and there is no loading bar, nothing. After a while, the filename changes from e.g, `Sent Items.partial.mbox` to `Sent Items.mbox` the export in mbox format is done (not that it'll silently fail if you attempt another export in the meantime -- just don't touch mail.app for a very long time). But when I re-imported it, it showed that it did not contain all emails (only roughly half).

However, after importing them, I got a message:

    Some messages could not be imported. The partially imported mailboxes are located in the mailbox named “Import” in the mailboxes list.

and indeed, I was lacking more than half of the mail in my archive mailbox

<img src="/wp-content/uploads/2022/06/Screen-Shot-2022-06-01-at-16.51.03-470x1024.png" class="wp-image-101" />

The export menu: I did it for all three mailbox with messages, and after the import some messages were missing, especially from Archive.

I'm not the first to report this issue, see this [stack exchange post](https://apple.stackexchange.com/questions/170560/how-to-export-all-emails-from-a-mailbox-in-apple-mail). I also tried to use Thunderbird and Microsoft Outlook without success.

### What worked

Method A From the above stack overflow post, one way is to create one folder per mailbox on the computer, then to select all message in each mailbox and to drag-n-drop them in this folder. This creates .eml files (one per mail, which include attachement).

This works (e.g in my archive folder, I get 10'243 .eml files, right in between Thunderbird number and Mail.app), and it is possible to import them back using the method described in the stack exchange post (File &gt; Import Mailbox &gt; From Apple Mail, then selecting the three folders). There is a delay when drag and dropping to export.

Method BAnother way is to identify the mailbox to be save in `~/Library/Mail/`V9. It's a string of numbers:` (base) ➜ `/Users/chadi/Library/Mail/V9` ls 17199DDE-A3A1-40C7-8FBB-662F004532AF` \# &lt;- this one is my EPFL mailbox ! `620B6005-3586-489C-AA7C-BBE9398CEA43` `E42160D9-B9F7-4677-B659-46CA4CAF9158 315CFCFE-F902-499E-BD53-259AC0F21BB6` `C6245073-FCAB-4DA4-A21C-A54693C7E882` `MailData 37C20BE2-E02F-48F5-91BA-2275086E138E` `CBB567A4-CD0F-4ED5-A5A0-6DAE30511627`

but I haven't found a proper way to find which one correspond to which inbox. I just got the folder size, found the one that were close to my inbox and then checked inside each folder to find in which my mails are.

Both way works. It takes much more space on disk (checking `~/Library/Mail/`V9 shows 9.21Gb instead of 4.36Gb for the original mail box). I like it because it keeps also keeps the conversation as... conversations, with each mail next to it's replies.

## Calendar

Calendar is way easier. Here I wanted to add my former institutional calendar to my google one, including all past events (and not just some from the last year, as copy-pasting and selecting all does).

I created a new calendar in google calendar. The, using Calendar.app, File &gt; export the former institutional calendar and then I imported it into the created calendar. As simple as that, but please control that events years ago are rightfully copied.

## The rest

Don't forget to check if you haven't left a document in the rest of institutional goods, such as:

-   Contacts
-   Institutional google drive, google docs, google sheets, google\*
-   storage
-   account on HPC clusters

and the list go one. With proper archiving practice it's quite easy to ensure if the git status of each repo is not ahead of the remote repository.

Please comment about your experience leaving institutional emails
