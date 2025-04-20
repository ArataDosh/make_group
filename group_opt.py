import random
import os
import csv
import itertools

def make_team(team_num, names):
    # チームの数とチームメンバーの名前を引数に、チーム案の一つを返す関数

    team_names = names.copy()
    team_list = []
    for t in range(len(team_num)):
        temp_team = random.sample(team_names, team_num[t])
        team_list.append(temp_team)
        for re in range(team_num[t]):
            team_names.remove(temp_team[re])

    return team_list

def asses_team(team_list, pair_count):
    # チームのリストとこれまで一緒のチームに入った回数を引数に、一緒のチームに入った回数(=損失)を計算する関数

    pair_count_dict = {
        frozenset([a, b]): count for a, b, count in pair_count
    }

    losses = 0

    for team in team_list:
        team_pairs = itertools.combinations(team, 2)
        for a, b in team_pairs:
            key = frozenset([a, b])
            losses += pair_count_dict.get(key, 0) 
    return losses


def commit_change(team_list,now_paircount):
    # チーム案を引数に取り、ペアになった回数をCSVファイルに記録する関数

    # まだペアのカウントを行ったことがない場合、ペアの全組み合わせをCSVファイルに入力する
    if now_paircount == []:
        name_course = []
        with open('member.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 2:
                    name_course.append([row[0].strip(), row[1].strip()])
        names = [member[0] for member in name_course]
        member_pair = {frozenset(pair) for pair in itertools.combinations(names, 2)}
        member_pair_list = [list(pair) for pair in member_pair]
        for member in member_pair_list:
            member.append(0)
        with open('pair_count.csv', 'w') as f:
            writer = csv.writer(f)   
            for m in member_pair_list:
                writer.writerow(m)
        now_paircount = []
        with open('pair_count.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                # 空行を除外し、2列ある行だけ追加
                now_paircount.append([row[0].strip(), row[1].strip(), int(row[2])])
        

    # 今回ペアになった組みあせをCSVファイルに記録する
    pairs = []
    for team in team_list:
        temp_pairs = {frozenset(pair) for pair in itertools.combinations(team, 2)}
        pairs.extend(temp_pairs)
    pairs_thistime_list = [list(pair) for pair in pairs]
    pairs_dict = {frozenset([a, b]): count for a, b, count in now_paircount}
    # ペアになった回数を+1する
    for a, b in pairs_thistime_list:
        key = frozenset([a, b])
        pairs_dict[key] += 1

    # 最後にCSVファイルに今回の結果を書き込んで処理を終了する
    updated_pairs_count = [[*pair, count] for pair, count in pairs_dict.items()]
    with open('pair_count.csv', 'w') as f:
        writer = csv.writer(f)
        for m in updated_pairs_count:
            writer.writerow(m)



if __name__ == '__main__':
    # 名簿が入ったCSVファイルから、名前をリスト形式にする
    name_course = []
    with open('member.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            # 空行を除外し、2列ある行だけ追加
            if len(row) == 2:
                name_course.append([row[0].strip(), row[1].strip()])
    names = [member[0] for member in name_course]


    # 現在までにペアになったことのある回数を取得する
    pair_count = []
    with open('pair_count.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            pair_count.append([row[0].strip(), row[1].strip(), int(row[2])])




    # 1000回試行し、最も一緒のチームに入った回数(=損失)が最も小さいグループを最良のグループとして提案する

    ####       チームそれぞれのメンバー数を入力
    team_num = [4, 4, 4, 4, 4, 5, 5, 5]
    ####

    try:
        if sum(team_num) != len(names):
            raise ValueError(f"メンバー数が一致しません。team_num の合計: {sum(team_num)}, names の数: {len(names)}")
        for i in range(1000):
            if i == 0:
                best_team = make_team(team_num, names)
                best_loss = asses_team(best_team, pair_count) 
                
            else:
                temp_team_prop = make_team(team_num , names)
                if asses_team(temp_team_prop, pair_count) < best_loss:
                    best_team = temp_team_prop
                    best_loss = asses_team(temp_team_prop, pair_count)

        # best_team を CSV に保存
        # with open('best_team_proposal.csv', 'w', newline='', encoding='utf-8') as f:
        #     writer = csv.writer(f)
        #     for team in best_team:
        #         writer.writerow(team)

        # print("最良チーム案:")
        # for i, team in enumerate(best_team, start=1):
        #     team_str = ", ".join(team)
        #     print(f"チーム{i}: {team_str}")
        # print(f'このチーム編成における損失は{best_loss}です。')

        commit_change(best_team,pair_count)
        
    except Exception as e:
        print("エラーが発生しました:", e)