def basketball_pro_tool():
    print("=== 🔥 PRO BASKETBALL BET TOOL (QUARTER MODE) ===")

    try:
        # Game type
        print("\nGame Type:")
        print("1 = NBA (12 min quarters)")
        print("2 = FIBA (10 min quarters)")
        choice = int(input("Choose (1/2): "))

        if choice == 1:
            quarter_time = 12
            total_game = 48
        elif choice == 2:
            quarter_time = 10
            total_game = 40
        else:
            print("Invalid choice")
            return

        # Quarter input
        quarter = int(input("Current Quarter (1-4): "))
        time_in_q = float(input("Time elapsed in current quarter: "))

        # Scores
        q1 = int(input("Q1 total score: "))
        q2 = int(input("Q2 total score: "))
        q3 = int(input("Q3 total score: "))
        q4 = int(input("Q4 total score (if not started = 0): "))

        line = float(input("Bookmaker line: "))

        # Total score
        total = q1 + q2 + q3 + q4

        # Time played
        minutes_played = (quarter - 1) * quarter_time + time_in_q
        time_left = total_game - minutes_played

        if minutes_played <= 0:
            print("Invalid time")
            return

        # 🔥 Current quarter pace (IMPORTANT)
        if quarter == 1:
            current_q_score = q1
        elif quarter == 2:
            current_q_score = q2
        elif quarter == 3:
            current_q_score = q3
        else:
            current_q_score = q4

        if time_in_q > 0:
            current_pace = current_q_score / time_in_q
        else:
            current_pace = 0

        # 🔥 Base pace
        base_pace = total / minutes_played

        # 🔥 Weighted pace (SMART)
        pace = (base_pace * 0.6) + (current_pace * 0.4)

        predicted = total + (pace * time_left)

        # 🔥 Quarter adjustment
        if quarter == 1:
            predicted *= 0.95
        elif quarter == 2:
            predicted *= 1.00
        elif quarter == 3:
            predicted *= 0.97
        elif quarter == 4:
            predicted *= 1.08  # strong foul boost

        diff = predicted - line

        # OUTPUT
        print("\n--- 📊 RESULT ---")
        print(f"Total Score: {total}")
        print(f"Predicted Final: {predicted:.2f}")
        print(f"Line: {line}")
        print(f"Difference: {diff:.2f}")

        # DECISION
        print("\n--- 🎯 DECISION ---")
        if diff >= 10:
            decision = "🔥 STRONG OVER"
        elif diff >= 5:
            decision = "👍 OVER"
        elif diff <= -10:
            decision = "🔥 STRONG UNDER"
        elif diff <= -5:
            decision = "👍 UNDER"
        else:
            decision = "⚖️ NO BET"

        print(decision)

        # 🔥 DOUBLE BET LOGIC
        print("\n--- 💰 DOUBLE BET ---")
        if abs(diff) >= 8 and quarter in [2, 3]:
            print("✅ SAFE TO DOUBLE BET")

            if "OVER" in decision:
                print("Bet 1: Over (higher line) → SMALL stake")
                print("Bet 2: Over (lower line) → BIG stake")
            elif "UNDER" in decision:
                print("Bet 1: Under (lower line) → SMALL stake")
                print("Bet 2: Under (higher line) → BIG stake")

            print("\nStake Example:")
            print("SMALL = 50")
            print("BIG = 150")

        else:
            print("❌ NO DOUBLE BET")

    except:
        print("❌ Input error - use numbers only")


# RUN
basketball_pro_tool()
