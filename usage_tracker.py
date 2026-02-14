import json
import os
from datetime import datetime, timedelta

class UsageTracker:
    def __init__(self, data_file="usage_stats.json"):
        self.data_file = data_file
        self.stats = self._load_data()
        
        # Approximate Costs per 1M Tokens (Input / Output)
        self.pricing = {
            "gpt-4o": (5.00, 15.00),
            "gpt-4o-mini": (0.15, 0.60),
            "gpt-4-turbo": (10.00, 30.00),
            "gpt-3.5-turbo": (0.50, 1.50),
            "dall-e-3": (0.040, 0.040), # Per Image (Standard 1024x1024) approx $0.04
            "gemini-1.5-flash": (0.075, 0.30), # Free tier exists, but pricing for paid
            "gemini-1.5-pro": (3.50, 10.50),
            "gemini-1.0-pro": (0.50, 1.50)
        }

    def _load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {"balance": 0.0}

    def _save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.stats, f, indent=4)

    def log_usage(self, provider, model, input_tokens, output_tokens, image_count=0):
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today not in self.stats:
            self.stats[today] = {"tokens_in": 0, "tokens_out": 0, "images": 0, "cost": 0.0}
            
        # Calculate Cost
        cost = 0.0
        if model in self.pricing:
            in_rate, out_rate = self.pricing[model]
            cost += (input_tokens / 1_000_000) * in_rate
            cost += (output_tokens / 1_000_000) * out_rate
            # DALL-E special case (image_count)
            if model == "dall-e-3":
                 cost += image_count * in_rate # Using first value as per-image cost for simplicity
        
        self.stats[today]["tokens_in"] += input_tokens
        self.stats[today]["tokens_out"] += output_tokens
        self.stats[today]["images"] += image_count
        self.stats[today]["cost"] += cost
        
        # Deduct from Balance
        if "balance" not in self.stats:
             self.stats["balance"] = 0.0
        self.stats["balance"] -= cost
        
        self._save_data()

    def get_daily_stats(self):
        today = datetime.now().strftime("%Y-%m-%d")
        return self.stats.get(today, {"tokens_in": 0, "tokens_out": 0, "images": 0, "cost": 0.0})

    def get_weekly_stats(self):
        total_tokens = 0
        total_images = 0
        total_cost = 0.0
        
        today = datetime.now()
        for i in range(7):
            day_str = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            if day_str in self.stats:
                day_data = self.stats[day_str]
                total_tokens += day_data["tokens_in"] + day_data["tokens_out"]
                total_images += day_data["images"]
                total_cost += day_data["cost"]
                
        return {"tokens": total_tokens, "images": total_images, "cost": total_cost}
    def set_balance(self, amount):
        self.stats["balance"] = float(amount)
        self._save_data()

    def get_balance(self):
        return self.stats.get("balance", 0.0)
