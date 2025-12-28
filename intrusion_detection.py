import psutil
import time
import statistics
import winsound
from datetime import datetime

# -----------------------------
# SETTINGS
# -----------------------------
BASELINE_SAMPLES = 15      # normal davranışı öyrənmək üçün
CHECK_INTERVAL = 1         # saniyə
ALERT_THRESHOLD = 2.0      # neçə dəfə normadan yuxarı olarsa alert

cpu_history = []

print("🔍 AI Real-Time Intrusion Detection Started")
print("📊 Learning normal CPU behavior...\n")

# -----------------------------
# BASELINE LEARNING
# -----------------------------
for i in range(BASELINE_SAMPLES):
    cpu = psutil.cpu_percent(interval=1)
    cpu_history.append(cpu)
    print(f"Learning {i+1}/{BASELINE_SAMPLES}: CPU = {cpu}%")

baseline_mean = statistics.mean(cpu_history)
baseline_std = statistics.stdev(cpu_history)

print("\n✅ Baseline learned")
print(f"Average CPU: {baseline_mean:.2f}%")
print(f"Std Dev: {baseline_std:.2f}%")
print("\n🟢 Monitoring started...\n")

# -----------------------------
# REAL-TIME MONITORING
# -----------------------------
while True:
    cpu = psutil.cpu_percent(interval=CHECK_INTERVAL)

    if baseline_std == 0:
        anomaly_score = 0
    else:
        anomaly_score = (cpu - baseline_mean) / baseline_std

    timestamp = datetime.now().strftime("%H:%M:%S")

    if anomaly_score > ALERT_THRESHOLD:
        print(f"🚨 [{timestamp}] ALERT! Abnormal CPU behavior detected!")
        print(f"   CPU: {cpu}% | Score: {anomaly_score:.2f}")

        # Sound alert
        winsound.Beep(1200, 700)

    else:
        print(f"[{timestamp}] CPU: {cpu}% | Status: NORMAL")

    time.sleep(0.5)
