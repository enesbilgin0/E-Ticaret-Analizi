import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Aşama 1: Veri Yükleme ve Hazırlık ---

try:
    df_baskets = pd.read_csv("basket_details.csv")
    df_customers = pd.read_csv("customer_details.csv")
except FileNotFoundError:
    print("Hata: Gerekli CSV dosyaları bulunamadı.")
    exit()

df_main = pd.merge(df_baskets, df_customers, on='customer_id', how='left')

df_main['basket_date'] = pd.to_datetime(df_main['basket_date'])
df_main['total_sale_volume'] = df_main['basket_count']


# --- Aşama 2: Keşifsel Veri Analizi ve Veri Temizliği ---

df_main['customer_age'].replace(df_main[df_main['customer_age'] > 100]['customer_age'].unique(), np.nan, inplace=True)
age_median_cleaned = df_main['customer_age'].median()

df_main['customer_age'].fillna(age_median_cleaned, inplace=True)
df_main['customer_age'] = df_main['customer_age'].astype('int')

missing_sex_perc = df_main['sex'].isnull().sum() / len(df_main) * 100
missing_tenure_perc = df_main['tenure'].isnull().sum() / len(df_main) * 100

print("--- Veri Hazırlık Raporu ---")
print(f"sex sütunundaki eksik değer oranı: {missing_sex_perc:.2f}%")
print(f"tenure sütunundaki eksik değer oranı: {missing_tenure_perc:.2f}%")
print("Yaş verisi temizlendi ve medyan ile dolduruldu.\n")


# --- Aşama 3: Veri Görselleştirme (Matplotlib) ---

print("Görseller oluşturuluyor...")

sales_over_time = df_main.set_index('basket_date')['total_sale_volume'].resample('D').sum().fillna(0)

plt.figure(figsize=(12, 6))
sales_over_time.plot(title='Zamana Göre Günlük Satış Hacmi')
plt.xlabel('Tarih')
plt.ylabel('Toplam Satış Hacmi (Adet)')
plt.grid(True)
plt.tight_layout()
plt.savefig('sales_over_time.png')
plt.close()
print("sales_over_time.png oluşturuldu.")


top_10_products = df_main.groupby('product_id')['total_sale_volume'].sum().nlargest(10)

plt.figure(figsize=(10, 6))
top_10_products.sort_values(ascending=True).plot(kind='barh', title='En Çok Satan İlk 10 Ürün (Satış Hacmi)')
plt.xlabel('Toplam Satış Hacmi (Adet)')
plt.ylabel('Ürün ID')
plt.tight_layout()
plt.savefig('top_10_products.png')
plt.close()
print("top_10_products.png oluşturuldu.\n")


# --- Aşama 4: Raporlama ---

print("--- Yönetim Raporu ---")

total_sales_volume = df_main['total_sale_volume'].sum()
start_date = df_main['basket_date'].min().strftime('%Y-%m-%d')
end_date = df_main['basket_date'].max().strftime('%Y-%m-%d')
date_range = f"{start_date} - {end_date}"

top_3_products_list = top_10_products.nlargest(3).reset_index()
top_3_products_list.columns = ['product_id', 'Toplam_Satış_Hacmi']

gender_distribution = df_main['sex'].value_counts(normalize=True).mul(100).to_dict()

print(f"Analiz Edilen Tarih Aralığı: {date_range}")
print(f"Toplam Satış Hacmi (Adet): {total_sales_volume}")
print("\nEn Çok Satan İlk 3 Ürün:")
print(top_3_products_list)
print("\nCinsiyet Dağılımı (Mevcut Kısıtlı Veri %0.48):")
print(gender_distribution)
print("\n--- Analiz Tamamlandı ---")