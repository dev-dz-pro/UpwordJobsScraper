import pickle

def get_job_features(top_box):
    job_features_list = []
    section = top_box.css('.up-card-section')[2]
    job_features = section.css('ul > li')
    for f in job_features:
        f1 = f.css('small ::text').get()
        if not f1 is None:
            v = f1.strip()
        else:
            v = ""
        f2 = f.css('div strong ::text').get()
        if not f2 is None:
            k = f2.strip()
        else:
            k = ""
        job_features_list.append(f'{" ".join(k.split())} - {" ".join(v.split())}')
    return job_features_list


def get_skills_expertise(top_box):
    skills_expertise = set()
    sections = top_box.css('.up-card-section')
    try:
        section_id = 5
        section = sections[section_id-1]
        skills_expertise_box = section.css('div > div > div')
    except:
        section_id = 6
        section = sections[section_id-1]
        skills_expertise_box = section.css('div > div > div')

    skills_expertise_box = skills_expertise_box.css('span')
    for spin in skills_expertise_box:
        q = " ".join(spin.css("span > a ::text").get().strip().replace('\n', '').replace('\t', '').replace('\r', '').split())
        if q != '':
            skills_expertise.add(q)
    return list(skills_expertise), section_id


def get_job_activities( top_box, section_id):
    activities = {}
    section = top_box.css('.up-card-section')[section_id]
    activities_on_this_job = section.css('ul > li')
    for activity in activities_on_this_job:
        if activity.xpath("text()").get().strip() != '':
            pre, kv =activity.css("span")[0].css("::text").get().strip(), " ".join(activity.xpath("text()").get().strip().split())
        else:
            try:
                pre, kv = activity.css("span")[0].css("::text").get().strip(), " ".join(activity.css("span")[-1].css("::text").get().strip().split())
            except:
                continue
        activities[pre] = kv
    return activities


def get_client_history(response):
    titles_history = []
    section = response.css('.work-history')
    client_histories = section.css('section > div')
    plus_more = section.css('footer::text').get()
    if not plus_more is None:
        plus_more = plus_more.strip()
    else:
        plus_more = "0"
    for client_history in client_histories:
        ch = client_history.css('div > h4 > span > a::text').get()
        if not ch is None:
            ch = ch.strip()
            title = " ".join(ch.strip().split())
        else:
            title = ""
        titles_history.append(title)
    return titles_history, f'Plus more {plus_more} works.'


def get_client_about(top_box, response):
    about_client = set()
    about_client_box = top_box.css('.cfe-ui-job-about-client')
    about_client_1 = response.css('.cfe-ui-job-about-client > div')
    for i, x in enumerate(about_client_1):
        if i > 0:
            dt = x.css("::text").extract()
            for y in dt:
                z = " ".join(str(y).split())
                if z != '' and z != 'Close the tooltip' and z != 'Learn how this affects your payment protection.' and z != 'About the client':
                    about_client.add(z)
    about_client_2 = about_client_box.css('ul > li')
    for x in about_client_2:
        dt = x.css("::text").extract()
        re_dt = " ".join(x.css("::text").extract()).strip()
        res = " ".join(re_dt.split())
        if res != '':
            about_client.add(res)
    return about_client


def save_qookie(response, filename):
    p_q = {}
    for x, y in response.request.headers.items():
        if x.decode('utf-8') == "Cookie":
            qq = y[0].decode('utf-8').split(';')
            for q in qq:
                x_y = q.strip().split('=')
                p_q[x_y[0]] = x_y[1]
            break

    for k, v in response.headers.items():
        if k.decode('utf-8') == 'Set-Cookie':
            for x in v:
                x_y = x.decode('utf-8').split(";")[0].strip().split("=")
                p_q[x_y[0]] = x_y[1]
            break

    pre_res = []
    for qk, qv in p_q.items():
        pre_res.append(f"{qk}={qv}")
        
    qookie = {"Cookie": '; '.join(pre_res)}
    with open(filename, 'wb') as handle:
        pickle.dump(qookie, handle, protocol=pickle.HIGHEST_PROTOCOL)
        

def load_qookie(filename):
    with open(filename, 'rb') as handle:
        qookie = pickle.load(handle)
    return qookie