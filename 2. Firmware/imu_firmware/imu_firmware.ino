#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;

const float alpha = 0.98; // Complementary filter constant
const float dt = 0.01;    // Loop time in sec

float ax, ay, az;
float gx, gy, gz;
float vx = 0, vy = 0;
float x = 0, y = 0;
float angle_gyro = 0, angle_accel = 0, angle = 0;

void setup() {
  Serial.begin(57600);
  Wire.begin();
  
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1);
  }
}

void loop() {
  unsigned long startTime = millis();

  sensors_event_t accel, gyro, temp;
  mpu.getEvent(&accel, &gyro, &temp);

  // Extract accelerometer data
  ax = accel.acceleration.x;
  ay = accel.acceleration.y;
  az = accel.acceleration.z;

  // Extract gyro data
  gx = gyro.gyro.x;
  gy = gyro.gyro.y;
  gz = gyro.gyro.z;

  // Calc angle from acc
  angle_accel = atan2(ay, az) * 180 / PI;

  // Integrate the gyroscope data -> angle_gyro
  angle_gyro += gx * dt;

  // Apply the complementary filter
  angle = alpha * (angle + gx * dt) + (1 - alpha) * angle_accel;

  // Correct acceleration by subtracting gravity component
  float ax_corrected = ax - sin(angle * PI / 180);
  float ay_corrected = ay - sin(angle * PI / 180);

  // integration acc > vel
  vx += ax_corrected * dt * 9.81;
  vy += ay_corrected * dt * 9.81;

  // displacement calc
  x += vx * dt;
  y += vy * dt;

  Serial.print(x);
  Serial.print(",");
  Serial.println(y);

  // Reset x and y
  x = 0;
  y = 0;

  // loop
  while (millis() - startTime < dt * 1000) {
    delay(1);
  }
}
