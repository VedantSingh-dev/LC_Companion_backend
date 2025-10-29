import requests
class leetcode_stats:
    def __init__(self,userName):
        self.userName=userName
        self.LEETCODE_GRAPHQL = "https://leetcode.com/graphql"
    
    def Question_Count(self):
        QUERY = """
        query userSessionProgress($username: String!) {
        matchedUser(username: $username) {
            submitStats {
            acSubmissionNum {
                difficulty
                count
            }
            }
        }
        }
        """
        payload = {
            "query": QUERY,
            "variables": {"username": self.userName},
            "operationName": "userSessionProgress",
        }
        r = requests.post(
            self.LEETCODE_GRAPHQL,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        data = r.json()
        ac_list = (
            data.get("data", {})
                .get("matchedUser", {})
                .get("submitStats", {})
                .get("acSubmissionNum", [])
        )
        result = {"easy": 0, "medium": 0, "hard": 0, "total": 0}
        for item in ac_list:
            diff = (item.get("difficulty") or "").lower()
            cnt = int(item.get("count") or 0)
            if diff in ("easy", "medium", "hard"):
                result[diff] = cnt
            elif diff == "all":
                result["total"] = cnt
        if result["total"] == 0:
                result["total"] = result["easy"] + result["medium"] + result["hard"]
        return result


    def Contest_History(self):
        QUERY = """
        query contestInfo($username: String!) {
        userContestRanking(username: $username) {
            rating
        }
        userContestRankingHistory(username: $username) {
            contest {
            title
            }
            problemsSolved
            attended
        }
        }
        """
        payload = {
            "query": QUERY,
            "variables": {"username": self.userName},
            "operationName": "contestInfo",
        }
        r = requests.post(
            self.LEETCODE_GRAPHQL,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        data = r.json()
        ranking = (data.get("data", {}) or {}).get("userContestRanking") or {}
        history = (data.get("data", {}) or {}).get("userContestRankingHistory") or []

        attended = [h for h in history if h.get("attended")]
        last_10 = attended[-10:]  
        contests = []
        for item in last_10:
            name = ((item.get("contest") or {}).get("title")) or ""
            solved = int(item.get("problemsSolved") or 0)
            contests.append({
                "contest_name": name,
                "questions_solved": solved
            })

        return {
            "overall_rating": float(ranking.get("rating") or 0.0),
            "contests": contests
        }

    def Topics(self):
        QUERY = """
        query skillStats($username: String!) {
        matchedUser(username: $username) {
            tagProblemCounts {
            fundamental { tagName tagSlug problemsSolved }
            intermediate { tagName tagSlug problemsSolved }
            advanced { tagName tagSlug problemsSolved }
            }
        }
        }
        """
        payload = {
            "query": QUERY,
            "variables": {"username": self.userName},
            "operationName": "skillStats",
        }
        r = requests.post(
            self.LEETCODE_GRAPHQL,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        data = r.json()

        tpc = (
            data.get("data", {})
                .get("matchedUser", {})
                .get("tagProblemCounts", {}) or {}
        )

        groups = []
        for key in ("fundamental", "intermediate", "advanced"):
            arr = tpc.get(key) or []
            groups.extend(arr)

        # If multiple groups contain the same tag, sum counts
        out = {}
        for it in groups:
            name = (it.get("tagName") or "").strip()
            if not name:
                continue
            out[name] = out.get(name, 0) + int(it.get("problemsSolved") or 0)
        return out

    def Last_accepted_submissions(self):
        QUERY = """
        query recentAccepted($username: String!) {
        recentAcSubmissionList(username: $username, limit: 20) {
            id
            title
            titleSlug
            timestamp
        }
        }
        """
        payload = {
        "query": QUERY,
        "variables": {"username": self.userName},
        "operationName": "recentAccepted",
        }
        r = requests.post(
            self.LEETCODE_GRAPHQL,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        data = r.json()
        items = (data.get("data", {}) or {}).get("recentAcSubmissionList", []) or []
        result = {}
        for i, it in enumerate(items, 1):
            title = it.get("title") or ""
            result[f"Q{i}"] = title
        return result
def main(userName):
    lc =leetcode_stats(userName)
    dic = {}
    dic['Questions_Solved']=lc.Question_Count()
    dic['Topicwise_Question_Solved']=lc.Topics()
    dic['Contest_History']=lc.Contest_History()
    dic['Last_20_Accepted_Submissions']=lc.Last_accepted_submissions()
    return dic

