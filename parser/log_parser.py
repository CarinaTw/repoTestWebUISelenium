import re
from collections import Counter
import json
import argparse


class LogParser:
    regexp_ip = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s'
    regexp_time = r'\sHTTP\/1.1"\s\d{3}\s\d*'
    regexp_status_code_4xx = r'\sHTTP\/1.1"\s(400|401|402|403|404|405|406|407|408|409|410|411|412|413|414|415|416|417)\s'
    regexp_status_code_5xx = r'\sHTTP\/1.1"\s(500|501|502|503|504|505)\s'
    filename = 'parser/statistics.json'

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--filename_original', help='Set file name to save statistic', default="access.log")
        parser.add_argument('--filename_result', help='Set file name to save statistic', default="results.json")

        args = parser.parse_args()

        self.file_name_log = args.filename_original
        self.file_name_res = args.filename_result

    @staticmethod
    def count_errors(err_list, status_code):
        cnt = 0
        for row in err_list:
            if row[0] == status_code:
                cnt = cnt + 1
        return status_code, cnt

    def reader(self):
        """
            Открывает на чтение файл логов и возвращает его содержимое (списком строк)
        """
        with open(self.file_name_log) as f:
            log = f.readlines()
        return log

    def count_requests_total(self):
        """
            Возвращает общее количество запросов
        """
        log_file = self.reader()

        ip_list = []
        for line in log_file:
            try:
                ip = re.findall(self.regexp_ip, line)
                ip_list.append(ip[0])
            except Exception:
                pass

        data_cnt = {"REQUESTS TOTAL COUNT": len(ip_list)}

        return data_cnt

    def count_request_by_method_type(self, method):
        """
            Возвращает кортеж количество запросов по типу: ('GET', 20) или ('POST', 10)
        """

        log_file = self.reader()

        met_list = []
        for line in log_file:
            try:
                met = re.findall(method, line)
                met_list.append(met[0])
            except Exception:
                pass

        data_cnt = {"METHOD": method, "COUNT": len(met_list)}

        return data_cnt

    def count_top_x_ip(self, cnt):
        """
            Возвращает список кортежей - топ х IP адресов, с которых были сделаны запросы:
            [('192.168.102.28 ', 5515), ('192.168.100.59 ', 2), ('192.168.102.29 ', 1)]
        """
        log_file = self.reader()

        ip_list = []
        for line in log_file:
            try:
                ip = re.findall(self.regexp_ip, line)
                ip_list.append(ip[0])
            except Exception:
                pass

        top_x_ip = Counter(ip_list).most_common(cnt)

        return {"MOST COMMON IPs": top_x_ip}

    def most_top_x_time_long_requests(self, cnt):
        """
           Возвращает топ X самых долгих запросов (должно быть видно метод, url, ip, время запроса)
        """
        log_file = self.reader()

        top_x_time = []
        for row in log_file:
            try:
                req_time = int(re.findall(self.regexp_time, row)[0][15:])
            except Exception:
                pass

            if len(top_x_time) < cnt:
                top_x_time.append((req_time, row))
                top_x_time.sort(reverse=True)

            elif len(top_x_time) >= cnt:
                top_x_time.sort(reverse=True)
                if req_time >= top_x_time[cnt - 1][0]:
                    top_x_time.pop(cnt - 1)
                    top_x_time.insert(cnt - 1, (req_time, row))

        top_x = []
        for i in range(len(top_x_time)):
            splitted = re.split(r'\s', top_x_time[i][1])
            top_x.append({"IP": splitted[0], "TIME": splitted[9], "METHOD": splitted[5], "URL": splitted[6]})

        return top_x

    def statistic_with_client_err_requests(self):
        """
            Возвращает сколько клиентских ошибок по типам (статус кодам)
                        и информацию по каждому запросу с клиентской ошибкой (status_code, ip, method, url)

        """

        log_file = self.reader()

        all_clnt_err = []
        for row in log_file:
            try:
                req_clnt_err = re.findall(self.regexp_status_code_4xx, row)
            except Exception:
                pass

            if req_clnt_err != []:
                if req_clnt_err[0] in ('400', '401', '402', '403', '404', '405', '406',
                                       '407', '408', '409', '410', '411', '412', '413', '414', '415', '416', '417'):
                    all_clnt_err.append((req_clnt_err[0], row))

        json_req_with_clnt_err = []
        for i in range(len(all_clnt_err)):
            splitted = re.split(r'\s', all_clnt_err[i][1])
            json_req_with_clnt_err.append(
                {"STATUS_CODE": splitted[8], "IP": splitted[0], "METHOD": splitted[5], "URL": splitted[10]})

        count_clnt_err = {}
        for i in range(len(all_clnt_err)):
            if all_clnt_err[i][0] not in count_clnt_err:
                count_clnt_err[all_clnt_err[i][0]] = 1
            elif all_clnt_err[i][0] in count_clnt_err:
                count_clnt_err[all_clnt_err[i][0]] = count_clnt_err[all_clnt_err[i][0]] + 1

        return count_clnt_err, json_req_with_clnt_err

    def statistic_with_server_err_requests(self):
        """
            Возвращает сколько ошибок сервера по типам (статус кодам)
                        и информацию по каждому запросу с серверной ошибкой (status_code, ip, method, url)

        """

        log_file = self.reader()

        all_srv_err = []
        for row in log_file:
            try:
                req_serv_err = re.findall(self.regexp_status_code_5xx, row)
            except Exception:
                pass

            if req_serv_err != []:
                if req_serv_err[0] in ('500', '501', '502', '503', '504', '505'):
                    all_srv_err.append((req_serv_err[0], row))

        json_req_with_serv_err = []
        for i in range(len(all_srv_err)):
            splitted = re.split(r'\s', all_srv_err[i][1])
            json_req_with_serv_err.append(
                {"STATUS_CODE": splitted[8], "IP": splitted[0], "METHOD": splitted[5], "URL": splitted[10]})

        count_serv_err = {}
        for i in range(len(all_srv_err)):
            if all_srv_err[i][0] not in count_serv_err:
                count_serv_err[all_srv_err[i][0]] = 1
            elif all_srv_err[i][0] in count_serv_err:
                count_serv_err[all_srv_err[i][0]] = count_serv_err[all_srv_err[i][0]] + 1

        return count_serv_err, json_req_with_serv_err

    def get_staistic_to_json(self):

        json_data = {"PARSER RESULTS": [
                        {"REQUESTS TOTAL COUNT": self.count_requests_total()["REQUESTS TOTAL COUNT"]},
                        {"METHODS GET/POST": [{"METHOD GET": self.count_request_by_method_type('GET')["COUNT"]},
                                              {"METHOD POST": self.count_request_by_method_type('POST')["COUNT"]}]},
                        {"MOST COMMON IPs (TOP 10)": self.count_top_x_ip(10)["MOST COMMON IPs"]},
                        {"TOP 10 TIME LONG REQUESTS": [self.most_top_x_time_long_requests(10)]},
                        {"CLIENT ERRORS": self.statistic_with_client_err_requests()},
                        {"SERVER ERRORS": self.statistic_with_server_err_requests()}
                    ]
                      }

        return json_data

    def write_data_to_json(self):
        to_json = self.get_staistic_to_json()
        with open(self.file_name_res, 'w') as f:
            f.write(json.dumps(to_json))


if __name__ == '__main__':
    pars = LogParser()
    pars.write_data_to_json()




