<b style="font-size:30px">TRÍCH XUẤT ĐẶC TRƯNG VÀ HUẤN LUYỆN MÔ HÌNH</b>
</br>
file  <i>CreateDatasetAndTrain_withpadding_HeNormal.ipynb</i>

<ol>
    <li>
        Thay đổi DATA_PATH trong code ở mục <b>3. Setup Folders for Collection</b> bằng đường dẫn đến dữ liệu:
        <br>
        <span>DATA_PATH = os.path.join('./drive/MyDrive/PBL5/Data/')</span>
    </li>
    <li>
        Run lần lượt các cell trong file đến mục <b>
5. Collect Keypoint Values for Training and Testing</b>  để tiến hành trích xuất đặc trưng từ video và lưu dữ liệu để train vào file <b>data_rich_full_padding.npz</b>
* nếu đã có file <b>data_rich_full_padding.npz</b> thì bỏ qua bước này,
    </li>
    <li>
    * Train model
        <ul>
            <li>
                Thay đổi các đường dẫn tới dữ liệu
               <br>
                DATA_PATH = os.path.join('./drive/MyDrive/PBL5/Data/')
               <br>
                log_dir = os.path.join(f'./drive/MyDrive/PBL5/Data/Logs/{time.time()}')
               <br>
                checkpoint_filepath = f'./drive/MyDrive/PBL5/Data/checkpoint/{time.time()}'
            </li>
            <li>
            Run lần lượt các cell trong mục <b>6 7</b> để tiến hành phân chia dữ liệu, huấn luyện mô hình.
            File weight được lưu ở <b>'{DATA_PATH}/weight_rich_padding_bs{batch_size}_lr{learning_rate}.h5'</b>
            </li>
        </ul>
    </li>
    ** Thực hiện các bước trên đã bao gồm các lệnh để các đặc các thư viện cần dùng, code sử dụng python 3.7.6
</ol>


</br>
<b style="font-size:30px">CHẠY SERVER</b><br>
thư mục  <i>Server</i>
<ol>
    <li>
        Sao chép file weight thu được khi huấn luyện mô hình vào folder server/app/weights 
    </li>
    <li>
        Thay thế <b>"./weights/weight_rich_padding_bs4_lr0.001_v2.h5"</b> trong file <b>/Server/app/setting.json</b> bằng đường dẫn đến weight vừa thêm.
    </li>
    </li>
        <ul> 
            <li>Mở terminal </li>
            <li>Chuyển thư mục làm việc đến thư mục <b>/Server/app/</b>
            <li>install docker-compose nếu chưa install</li>
            <li>run  <b>docker-compose up</b> để chạy server
            </li>
            <li>Có thể test API ở 2 địa chỉ <b>{root_url}/LSTM</b> và <b>{root_url}/LSTM/single</b>. Đầu vào của 2 api là 1 file video, kết quả là văn bản tương ứng với hành động.
            </li>
        </ul>
    </li>
</ol>
