import requests
import time
import re
import random
import string
import os

REFERRAL_CODE = "TRUTH-9EBG7TYV" # Change it with yours.

class AutoRefTruthTensor:
    def __init__(self, referral_code: str):
        self.referral_code = referral_code
        self.mail_tm_base = "https://api.mail.tm"
        self.truth_tensor_base = "https://api.truthtensor.com"
        self.truth_tensor_agent = "https://seeker.truthtensor.com"
        self.proxies = self.load_proxies()
        self.current_proxy_index = 0
        self.truth_tensor_headers = {
            'accept': '*/*',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://truthtensor.com',
            'referer': 'https://truthtensor.com/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
            'x-app-origin': 'https://truthtensor.com'
        }
    
    def load_proxies(self):
        try:
            if os.path.exists('proxy.txt'):
                with open('proxy.txt', 'r') as f:
                    proxies = [line.strip() for line in f if line.strip()]
                if proxies:
                    print(f"✅ Loaded {len(proxies)} proxies from proxy.txt")
                    return proxies
        except Exception as e:
            print(f"⚠️  Error loading proxies: {e}")
        return []
    
    def get_next_proxy(self):
        if not self.proxies:
            return None
        
        proxy = self.proxies[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
        
        if not proxy.startswith('http'):
            if proxy.count(':') >= 3:
                parts = proxy.split(':')
                proxy = f"http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
            else:
                proxy = f"http://{proxy}"
        
        return {
            'http': proxy,
            'https': proxy
        }
        
    def generate_username(self):
        consonants = 'bcdfghjklmnpqrstvwxyz'
        vowels = 'aeiou'
        length = random.randint(8, 12)
        
        username = ''
        for i in range(length):
            if i % 2 == 0:
                username += random.choice(consonants)
            else:
                username += random.choice(vowels)
        
        return username.capitalize()
    
    def generate_agents_data(self, username: str, user_id: str):
        suffix = random.choice([
            "Crypto", "Trade", "Invest", "Capital", "Wealth", "Finance",
            "Market", "Alpha", "Quantum", "Oracle", "Vanguard", "Apex",
            "Fortune", "Prosper", "Bull", "Bear", "Hedge", "Portfolio",
            "AI", "Neural", "Synth", "Cybernetic", "Digital", "Logic",
            "Algorithm", "Vector", "Matrix", "Node", "Core", "Protocol",
            "Quantum", "Byte", "Code", "Circuit", "Data", "Analytics",
            "Pro", "Expert", "Master", "Guru", "Specialist", "Analyst",
            "Strategist", "Advisor", "Manager", "Engineer", "Architect",
            "Phoenix", "Wolf", "Falcon", "Dragon", "Titan", "Vortex",
            "Storm", "Zenith", "Nova", "Orbit", "Galaxy", "Cosmic",
            "Elite", "Prime", "Ultra", "Nexus", "Fusion", "Dynamic",
            "Vision", "Pulse", "Edge", "Peak", "Flow", "Momentum",
            "Genesis", "Legacy", "Evolution", "Revolution",
            "Commando", "Sentry", "Guardian", "Sentinel", "Watchman",
            "Strategos", "Tactician", "Operator", "Recon", "Scout",
            "Merlin", "Oracle", "Prophet", "Sage", "Wizard", "Enigma"
        ])
        
        agent_name = f"{username} {suffix}"

        timestamp = int(time.time()) * 1000
        strategy_id = f"user-{user_id.lower()}-{timestamp}"

        agent_model = random.choice([
            "google/gemini-3-pro-preview",
            "qwen/qwen3-max",
            "openai/gpt-5.1",
            "x-ai/grok-4",
            "deepseek/deepseek-chat-v3.1",
            "anthropic/claude-sonnet-4.5",
            "moonshotai/kimi-k2-thinking",
            "minimax/minimax-m2"
        ])

        return {
            "name": agent_name,
            "strategy_id": strategy_id,
            "model": agent_model,
        }
    
    def get_mail_domain(self):
        try:
            proxies = self.get_next_proxy()
            response = requests.get(
                f"{self.mail_tm_base}/domains",
                proxies=proxies,
                timeout=30
            )
            response.raise_for_status()
            domains = response.json()['hydra:member']
            return domains[0]['domain'] if domains else None
        except Exception as e:
            print(f"❌ Error getting domain: {e}")
            return None
    
    def create_temp_email(self, username: str, domain: str):
        try:
            email = f"{username.lower()}@{domain}"
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            
            proxies = self.get_next_proxy()
            response = requests.post(
                f"{self.mail_tm_base}/accounts",
                json={
                    "address": email,
                    "password": password
                },
                proxies=proxies,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            return {
                "email": data['address'],
                "password": password,
                "id": data['id']
            }
        except Exception as e:
            print(f"❌ Error creating email: {e}")
            return None
    
    def get_auth_token(self, email: str, password: str):
        try:
            proxies = self.get_next_proxy()
            response = requests.post(
                f"{self.mail_tm_base}/token",
                json={
                    "address": email,
                    "password": password
                },
                proxies=proxies,
                timeout=30
            )
            response.raise_for_status()
            return response.json()['token']
        except Exception as e:
            print(f"❌ Error getting token: {e}")
            return None
    
    def register_account(self, email: str, username: str):
        try:
            payload = {
                "email": email,
                "username": username,
                "referral_code": self.referral_code,
                "terms_accepted": True
            }
            
            proxies = self.get_next_proxy()
            response = requests.post(
                f"{self.truth_tensor_base}/auth/signup",
                json=payload,
                headers=self.truth_tensor_headers,
                proxies=proxies,
                timeout=30
            )
            
            data = response.json()
            
            if response.ok and data.get('success'):
                return {"success": True, "data": data}
            else:
                return {"success": False, "error": data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def extract_verification_link(self, html_content: str):
        patterns = [
            r'https://[a-f0-9]+\.us-east-1\.resend-links\.com/[^\s"<>]+',
            r'https://truthtensor\.com/verify-email\?token=[a-f0-9-]+',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html_content)
            if match:
                link = match.group(0)
                
                token_match = re.search(r'token=([a-f0-9-]+)', link)
                if token_match:
                    return token_match.group(1)
        return None
    
    def wait_for_verification_email(self, token: str, max_attempts: int = 30):
        print("⏳ Wait for email verification...")
        
        for attempt in range(max_attempts):
            try:
                proxies = self.get_next_proxy()
                response = requests.get(
                    f"{self.mail_tm_base}/messages",
                    headers={"Authorization": f"Bearer {token}"},
                    proxies=proxies,
                    timeout=30
                )
                
                if response.ok:
                    messages = response.json()['hydra:member']
                    
                    for msg in messages:
                        if msg['from']['address'] == 'truthtensor@verify.inferencelabs.com':
                            msg_response = requests.get(
                                f"{self.mail_tm_base}/messages/{msg['id']}",
                                headers={"Authorization": f"Bearer {token}"},
                                proxies=proxies,
                                timeout=30
                            )
                            
                            if msg_response.ok:
                                msg_data = msg_response.json()
                                html_content = msg_data.get('html', [msg_data.get('text', [''])])[0]
                                
                                verification_token = self.extract_verification_link(html_content)
                                if verification_token:
                                    return verification_token
                
                time.sleep(3)
                print(f"   Attempt {attempt + 1}/{max_attempts}...")
                
            except Exception as e:
                print(f"❌ Error checking inbox: {e}")
                time.sleep(3)
        
        return None
    
    def verify_email(self, token: str):
        try:
            proxies = self.get_next_proxy()
            response = requests.get(
                f"{self.truth_tensor_base}/auth/verify-email",
                params={"token": token},
                headers=self.truth_tensor_headers,
                proxies=proxies,
                timeout=30
            )
            
            data = response.json()
            
            if response.ok and data.get('success'):
                return {"success": True, "data": data}
            else:
                return {"success": False, "error": data}
        except Exception as e:
            return {"success": False, "error": str(e)}
        
    def create_agent(self, jwt_token: str, agents_data: dict):
        try:
            payload = {
                "config": {
                    "version": "1.0",
                    "strategy_id": agents_data['strategy_id'],
                    "name": agents_data['name'],
                    "description": "",
                    "model": agents_data['model'],
                    "execution": {
                        "interval_minutes": 60,
                        "max_markets_per_cycle": 50,
                        "triggers": [
                            {
                                "type": "temporal",
                                "enabled": True,
                                "config": {
                                    "interval_minutes": 60
                                }
                            }
                        ]
                    },
                    "data_sources": {
                        "markets": {
                            "enabled": True
                        },
                        "news": {
                            "enabled": True,
                            "window_minutes": 60,
                            "max_headlines": 30
                        },
                        "portfolio": {
                            "enabled": True,
                            "include_open_positions": True,
                            "include_historical": True,
                            "max_historical_trades": 30
                        }
                    },
                    "context": {
                        "template": "portfolio"
                    },
                    "prompt": {
                        "system_template": "",
                        "user_template": "You are a careful trader. Before making any trade:\n1. Look at the news - is there anything important happening?\n2. Check your current positions - do any need to be closed?\n3. Only buy if you're at least 60% confident you're right\n4. Never risk more than you can afford to lose\n\nWhen you're unsure, it's okay to wait and do nothing.\n\nCURRENT TIME: {{currentTime}}\n\nPORTFOLIO STATUS:\n- Available Cash: {{currency portfolio.availableCapital}}\n- Money Invested: {{currency portfolio.deployedCapital}}\n- Total Value: {{currency portfolio.totalCapital}}\n- Open Positions: {{length portfolio.openPositions}}\n\n{{#if portfolio.openPositions}}\nYOUR CURRENT POSITIONS:\n{{#each portfolio.openPositions}}\n[{{this.conditionId}}] {{this.market}}\n  You own: {{this.side}} @ {{percentage this.entryPrice 1}}\n  Opened: {{isoDate this.openedAt}}\n  Profit/Loss: {{currency this.unrealizedPnl}}\n{{/each}}\n{{/if}}\n\n{{#if news.headlines}}\nRECENT NEWS:\n{{#each news.headlines}}\n- [{{this.source}}] {{this.title}} ({{timeAgo this.pubDate}})\n{{/each}}\n{{/if}}\n\n{{#if markets.markets}}\nMARKETS YOU CAN TRADE:\n{{#each markets.markets}}\n[{{this.conditionId}}] {{this.question}}\n  YES price: {{percentage this.yesPrice 1}} | NO price: {{percentage this.noPrice 1}}\n  Closes: {{isoDate this.endDate}}\n{{/each}}\n{{/if}}",
                        "variables": {}
                    },
                    "trading": {
                        "position_sizing": {
                            "method": "fixed_percentage",
                            "percentage": 1,
                            "min_amount": 2
                        },
                        "risk_management": {
                            "max_open_positions": 1
                        }
                    },
                    "model_params": {
                        "temperature": 0.7,
                        "max_tokens": 1000
                    }
                },
                "active": False
            }

            headers = self.truth_tensor_headers.copy()
            headers["authorization"] = f"Bearer {jwt_token}"

            proxies = self.get_next_proxy()
            response = requests.post(
                f"{self.truth_tensor_agent}/strategies",
                json=payload,
                headers=headers,
                proxies=proxies,
                timeout=30
            )
            
            data = response.json()
            
            if response.ok:
                return {"success": True, "data": data}
            else:
                return {"success": False, "error": data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_account(self):
        print("\n" + "="*60)
        
        username = self.generate_username()
        print(f"👤 Username: {username}")
        
        domain = self.get_mail_domain()
        if not domain:
            return {"success": False, "error": "Failed to get mail domain"}
        
        email_data = self.create_temp_email(username, domain)
        if not email_data:
            return {"success": False, "error": "Failed to create email"}
        
        email = email_data['email']
        print(f"📧 Email   : {email}")
        
        mail_token = self.get_auth_token(email, email_data['password'])
        if not mail_token:
            return {"success": False, "error": "Failed to get mail token"}
        
        print("📝 Registering account...")
        reg_result = self.register_account(email, username)
        
        if not reg_result['success']:
            print(f"❌ Registration failed: {reg_result.get('error', 'Unknown error')}")
            return reg_result
        
        reg_data = reg_result['data']
        user_id = reg_data.get('user_id', 'N/A')
        print(f"✅ Registration successful!")
        print(f"   User ID: {user_id}")
        print(f"   Message: {reg_data.get('message', 'N/A')}")
        
        verification_token = self.wait_for_verification_email(mail_token)
        
        if not verification_token:
            print("❌ Verification email not received")
            return {"success": False, "error": "Verification email timeout"}
        
        print(f"🔑 Verification token: {verification_token}")
        
        print("✉️  Verifying email...")
        verify_result = self.verify_email(verification_token)
        
        if not verify_result['success']:
            print(f"❌ Email verification failed: {verify_result.get('error', 'Unknown error')}")
            return verify_result
        
        verify_data = verify_result['data']
        user_data = verify_data.get('user', {})
        jwt_token = verify_data.get('jwt', 'N/A')
        
        print(f"✅ Email verified successfully!")
        print(f"   Username: {user_data.get('username', 'N/A')}")
        print(f"   Email   : {user_data.get('email', 'N/A')}")
        print(f"   Ref Code: {user_data.get('referral_code', 'N/A')}")

        print("🤖 Creating agent...")
        agents_data = self.generate_agents_data(username, user_id)

        agent = self.create_agent(jwt_token, agents_data)
        
        if not agent['success']:
            print(f"❌ Create agent failed: {agent.get('error', 'Unknown error')}")
            return agent

        print(f"✅ Agent created successfully!")
        print(f"   Agent Name : {agents_data.get('name', 'N/A')}")
        print(f"   Strategy Id: {agents_data.get('strategy_id', 'N/A')}")
        print(f"   Agent Model: {agents_data.get('model', 'N/A')}")
        
        return {
            "success": True,
            "username": username,
            "email": email,
            "referral_code": user_data.get('referral_code'),
            "verified": True
        }
    
    def run(self, total_accounts: int = 1, delay_between: int = 5):
        print(f"🎯 Referral Code: {self.referral_code}")
        print(f"🔢 Total Accounts: {total_accounts}")
        print(f"⏱️  Delay Between: {delay_between}s")
        
        success_count = 0
        failed_count = 0
        
        for i in range(total_accounts):
            print(f"\n🚀 Creating account {i + 1}/{total_accounts}...")
            
            result = self.create_account()
            
            if result['success']:
                success_count += 1
                print(f"✅ Account {i + 1} created successfully!")
            else:
                failed_count += 1
                print(f"❌ Account {i + 1} failed: {result.get('error', 'Unknown error')}")
            
            if i < total_accounts - 1:
                print(f"\n⏳ Waiting {delay_between} seconds before next account...")
                time.sleep(delay_between)
        
        print("\n" + "="*60)
        print(f"""
╔══════════════════════════════════════════════════════════╗
║                    SUMMARY                               ║
╠══════════════════════════════════════════════════════════╣
║  ✅ Success: {success_count:<2}                                        ║
║  ❌ Failed:  {failed_count:<2}                                        ║
║  📊 Total:   {total_accounts:<2}                                        ║
╚══════════════════════════════════════════════════════════╝
        """)


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════╗
║          AUTO REFERRAL TRUTHTENSOR - VONSSY              ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    try:
        TOTAL_ACCOUNTS = int(input("🔢 Number of accounts you want to create: ").strip())
        if TOTAL_ACCOUNTS < 1:
            print("❌ Minimum number of accounts is 1!")
            exit(1)
    except ValueError:
        print("❌ Enter a valid number!")
        exit(1)
    
    DELAY_BETWEEN = 5
    
    bot = AutoRefTruthTensor(REFERRAL_CODE)
    bot.run(total_accounts=TOTAL_ACCOUNTS, delay_between=DELAY_BETWEEN)