# 1101-210025 計算機組織與結構 期末Project Cache-Simulator

**這個程式是一個快取記憶體模擬器，模擬 CPU 存取記憶體時，快取讀取和替換的運作機制，並計算 Hit Rate。**

程式首先會讀取文檔 2way_input.txt、4way_input.txt 中的前四行

machine(in bits)：決定 CPU 可尋址空間的總位元數。

total_cache_size(in KB)：定義快取記憶體的總容量，單位為 KB。

num_cache_way：決定每個 Set 中快取行的數量。

block_size(in bytes)：定義每個 Cache 的大小，單位為 Bytes。

在完成快取參數的設定後，R 94e20 代表對十六進制位址 0x94e20 執行讀取操作。

## 進行模擬時程式會執行以下核心步驟

位址分解： 程式首先將這個十六進制位址轉換為完整的 64 位元二進制格式。隨後，該 64 位元位址會根據計算好的位元長度，切割成 Tag、Index 和 Block Offset 三個部分。

快取操作： 程式利用 Index 找到對應的 Set，並檢查該 Set 中是否存在與位址 Tag 相符的。

替換機制： 若發生快取不命中（Miss），且該 Set 中的所有 Way 滿載，程式會根據配置可選的 LRU 或 FIFO 選擇其中一個 Way 進行替換，將新的 Tag 寫入該位置。

## 所有模擬結果和統計數據將會詳細記錄在 output.txt 檔案中

### 快取參數

num_set: 快取中的集合總數。

num_block_offset_bit: 區塊位移的位元長度。

num_index_bit: 索引的位元長度。

num_tag_bit: 標籤的位元長度。

### 執行期間的統計數據

num_total_access: 總記憶體存取次數。

num_hit: 快取命中次數。

num_miss: 快取不命中次數。

hit_rate: 最終計算所得的快取命中率。

### hit trace

hit trace 會逐行記錄每一次 hit，包括存取指令、命中的 Index 和 Way。
