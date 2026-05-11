#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复 aitrainer 所有缺打分逻辑的题目。
策略：
1. 在 .btn-group 后、<script> 前插入 scoreResult + answerComparison div
2. 在 </script> 前插入完整打分逻辑（包含 fuzzyMatch、scoring 数组、btnCheck/btnReset 绑定）
"""
import os, re

BASE = r"C:\Users\76272\Documents\GitHub\aitrainer"

# ══════════════════════════════════════════════════════
# 每道题的打分配置：{ id: [{ id, ans, score, hint }], max, textItems? }
# textItems: textarea半分项 { id, keywords, score }
# ══════════════════════════════════════════════════════
SCORING_MAP = {

# ── 2.1.4 医疗研究数据清洗（15分代码+5分规范=总20分，但题目QMAX=0，改为20）
"2.1.4": {
    "max": 20,
    "items": [
        {"id":"b1","ans":"pd.read_csv('2.1.4_train.csv', encoding='gbk')","score":1,"hint":"read_csv 并指定 encoding='gbk'"},
        {"id":"b2","ans":"data.info()","score":1,"hint":"data.info() 查看表结构"},
        {"id":"b3","ans":"rename","score":1,"hint":"data.rename(...)"},
        {"id":"b4","ans":"{'病人 ID': '患者 ID'}","score":1,"hint":"字典映射 {'病人 ID': '患者 ID'}"},
        {"id":"b5","ans":"data['诊断日期'] - data['就诊日期']","score":1,"hint":"诊断日期 - 就诊日期"},
        {"id":"b6","ans":"data","score":0,"hint":""},
        {"id":"b7","ans":"data['诊断延迟']","score":1,"hint":"过滤诊断延迟>=0"},
        {"id":"b8","ans":"data['病程']","score":1,"hint":"过滤病程>0"},
        {"id":"b9","ans":"data['年龄']","score":1,"hint":"过滤年龄<120"},
        {"id":"b10","ans":"data.drop_duplicates","score":1,"hint":"drop_duplicates(inplace=True)"},
        {"id":"b11","ans":"'年龄', '体重', '身高'","score":1,"hint":"归一化列：年龄、体重、身高"},
        {"id":"b12","ans":"scaler.fit_transform(data[columns_to_normalize])","score":1,"hint":"scaler.fit_transform(...)"},
        {"id":"b13","ans":"treatment_outcome_distribution.plot","score":1,"hint":"调用 .plot(kind='bar')"},
        {"id":"b14","ans":"kind='bar'","score":0,"hint":""},
        {"id":"b15","ans":"plt.scatter","score":1,"hint":"plt.scatter(x, y)"},
        {"id":"b16","ans":"data['年龄']","score":0,"hint":""},
        {"id":"b17","ans":"data['疾病严重程度']","score":0,"hint":""},
        {"id":"b18","ans":"data.to_csv","score":1,"hint":"data.to_csv(output_path, index=False)"},
        {"id":"b19","ans":"index=False","score":0,"hint":""},
    ],
    "textItems": [
        {"id":"washNorm","keywords":["缺失","删除","重复","归一化","标准化","数据类型"],"score":3,"hint":"数据清洗规范"},
        {"id":"labelNorm","keywords":["标注","类别","标签","规则"],"score":2,"hint":"数据标注规范"},
    ]
},

# ── 2.1.5 燃油效率数据清洗（15分代码+5分规范=20分）
"2.1.5": {
    "max": 20,
    "items": [
        {"id":"b1","ans":"pd.read_csv('auto-mpg.csv')","score":1,"hint":"read_csv 加载数据集"},
        {"id":"b2","ans":"data.head()","score":1,"hint":"显示前五行"},
        {"id":"b3","ans":"data.isnull().sum()","score":1,"hint":"显示空缺值数量"},
        {"id":"b4","ans":"data.dropna()","score":2,"hint":"dropna() 删除缺失行"},
        {"id":"b5","ans":"pd.to_numeric","score":1,"hint":"pd.to_numeric(..., errors='coerce')"},
        {"id":"b6","ans":"data_cleaned['Your age']","score":0,"hint":""},
        {"id":"b7","ans":"astype(int)","score":1,"hint":"astype(int) 转整数"},
        {"id":"b8","ans":"data_cleaned.drop_duplicates()","score":1,"hint":"drop_duplicates()"},
        {"id":"b9","ans":"'How do you describe your current level of fitness ?'","score":1,"hint":"列名带空格"},
        {"id":"b10","ans":"label_encoder.fit_transform(data_cleaned['How do you describe your current level of fitness ?'])","score":1,"hint":"fit_transform 编码"},
        {"id":"b11","ans":"exercise_frequency_counts.plot.pie","score":1,"hint":"pie 饼图"},
        {"id":"b12","ans":"train_test_split","score":1,"hint":"train_test_split(...)"},
        {"id":"b13","ans":"data_filled, test_size=0.2","score":1,"hint":"test_size=0.2"},
        {"id":"b14","ans":"'2.1.5_cleaned_data.csv'","score":1,"hint":"文件名 2.1.5_cleaned_data.csv"},
        {"id":"b15","ans":"train_data.to_csv","score":0,"hint":""},
        {"id":"b16","ans":"cleaned_file_path","score":0,"hint":""},
    ],
    "textItems": [
        {"id":"washNorm","keywords":["缺失","删除","重复","归一化","标准化","异常"],"score":3,"hint":"数据清洗规范"},
        {"id":"labelNorm","keywords":["标注","类别","标签","规则","目标"],"score":2,"hint":"数据标注规范"},
    ]
},

# ── 2.2.1 Logistic回归（20分：M1-M11代码17分+M12答题纸3分）
"2.2.1": {
    "max": 20,
    "items": [
        {"id":"M1_1","ans":"pd.read_csv('finance.csv')","score":1,"hint":"read_csv 加载数据"},
        {"id":"M1_2","ans":"data.head()","score":1,"hint":"显示前五行"},
        {"id":"M2","ans":"train_test_split(X, y, test_size=0.2, random_state=42)","score":1,"hint":"train_test_split(X,y,test_size=0.2,random_state=42)"},
        {"id":"M3","ans":"LogisticRegression(max_iter=1000)","score":2,"hint":"LogisticRegression(max_iter=1000)"},
        {"id":"M4","ans":"model.fit(X_train, y_train)","score":2,"hint":"model.fit(X_train, y_train)"},
        {"id":"M5","ans":"dump(model, file)","score":1,"hint":"pickle.dump(model, file)"},
        {"id":"M6","ans":"model.predict(X_test)","score":1,"hint":"model.predict(X_test)"},
        {"id":"M7","ans":"accuracy_score(y_test, y_pred)","score":2,"hint":"accuracy_score(y_test, y_pred)"},
        {"id":"M8","ans":"smote.fit_resample(X_train, y_train)","score":2,"hint":"smote.fit_resample(X_train, y_train)"},
        {"id":"M9","ans":"model.fit(X_resampled, y_resampled)","score":2,"hint":"model.fit(X_resampled, y_resampled)"},
        {"id":"M10","ans":"model.predict(X_test)","score":1,"hint":"model.predict(X_test)"},
        {"id":"M11","ans":"accuracy_score(y_test, y_pred_resampled)","score":1,"hint":"accuracy_score(y_test, y_pred_resampled)"},
    ],
    "textItems": [
        {"id":"errorAnalysis","keywords":["过拟合","欠拟合","精确","召回","数据不平衡","错误","分析"],"score":1,"hint":"错误分析"},
        {"id":"improveSuggest","keywords":["增加","调整","优化","改进","特征","数据"],"score":1,"hint":"改进建议"},
    ]
},

# ── 2.2.2 随机森林线性回归（20分：M1-M13代码17分+M14答题3分）
"2.2.2": {
    "max": 20,
    "items": [
        {"id":"M1_1","ans":"pd.read_csv('auto-mpg.csv', na_values='?')","score":1,"hint":"read_csv 并设 na_values='?'"},
        {"id":"M1_2","ans":"df.head()","score":1,"hint":"df.head()"},
        {"id":"M2_1","ans":"pd.to_numeric","score":1,"hint":"pd.to_numeric(df['horsepower'], errors='coerce')"},
        {"id":"M2_2","ans":"df['horsepower']","score":0,"hint":""},
        {"id":"M2_3","ans":"df.dropna()","score":1,"hint":"df.dropna()"},
        {"id":"M3_1","ans":"df[['cylinders','displacement','horsepower','weight','acceleration','model_year','origin']]","score":1,"hint":"选择7个特征列"},
        {"id":"M3_2","ans":"df['mpg']","score":1,"hint":"df['mpg']"},
        {"id":"M4_1","ans":"train_test_split","score":0,"hint":""},
        {"id":"M4_2","ans":"X, y, test_size=0.2","score":1,"hint":"test_size=0.2"},
        {"id":"M5_1","ans":"Pipeline","score":1,"hint":"Pipeline([...])"},
        {"id":"M5_2","ans":"StandardScaler()","score":0,"hint":""},
        {"id":"M5_3","ans":"LinearRegression()","score":1,"hint":"LinearRegression()"},
        {"id":"M6","ans":"pipeline.fit(X_train, y_train)","score":1,"hint":"pipeline.fit(X_train, y_train)"},
        {"id":"M7","ans":"dump(pipeline, model_file)","score":1,"hint":"pickle.dump(pipeline, model_file)"},
        {"id":"M8","ans":"pipeline.predict(X_test)","score":1,"hint":"pipeline.predict(X_test)"},
        {"id":"M9","ans":"results_df.to_csv","score":1,"hint":"results_df.to_csv(...)"},
        {"id":"M10_1","ans":"RandomForestRegressor","score":0,"hint":""},
        {"id":"M10_2","ans":"n_estimators=100","score":1,"hint":"n_estimators=100"},
        {"id":"M11","ans":"rf_model.fit(X_train, y_train)","score":1,"hint":"rf_model.fit(X_train, y_train)"},
        {"id":"M12","ans":"rf_model.predict(X_test)","score":1,"hint":"rf_model.predict(X_test)"},
        {"id":"M13","ans":"results_rf_df.to_csv","score":1,"hint":"results_rf_df.to_csv(...)"},
    ],
    "textItems": [
        {"id":"errorAnalysis","keywords":["过拟合","欠拟合","精确","误差","R²","分析"],"score":1,"hint":"错误分析"},
        {"id":"improveSuggest","keywords":["增加","调整","优化","改进","特征"],"score":1,"hint":"改进建议"},
    ]
},

# ── 2.2.3 随机森林+XGBoost（20分）
"2.2.3": {
    "max": 20,
    "items": [
        {"id":"M1_1","ans":"pd.read_csv('fitness_data.csv')","score":1,"hint":"read_csv 加载数据"},
        {"id":"M1_2","ans":"df.head()","score":1,"hint":"df.head()"},
        {"id":"M2_1","ans":"pd.get_dummies","score":1,"hint":"pd.get_dummies(X)"},
        {"id":"M2_2","ans":"df['Your age'].apply","score":1,"hint":"apply(lambda x: int(x.split(' ')[0]))"},
        {"id":"M3_1","ans":"train_test_split","score":0,"hint":""},
        {"id":"M3_2","ans":"X, y, test_size=0.2","score":1,"hint":"test_size=0.2"},
        {"id":"M4_1","ans":"RandomForestRegressor","score":0,"hint":""},
        {"id":"M4_2","ans":"n_estimators=100","score":1,"hint":"n_estimators=100"},
        {"id":"M5","ans":"rf_model.fit(X_train, y_train)","score":1,"hint":"rf_model.fit(X_train, y_train)"},
        {"id":"M6","ans":"dump(rf_model, model_file)","score":1,"hint":"pickle.dump(rf_model, model_file)"},
        {"id":"M7","ans":"rf_model.predict(X_test)","score":1,"hint":"rf_model.predict(X_test)"},
        {"id":"M8_1","ans":"rf_model.score(X_train, y_train)","score":0,"hint":""},
        {"id":"M8_2","ans":"rf_model.score(X_test, y_test)","score":1,"hint":"rf_model.score(X_test, y_test)"},
        {"id":"M9","ans":"mean_squared_error(y_test, y_pred)","score":1,"hint":"mean_squared_error(y_test, y_pred)"},
        {"id":"M10","ans":"r2_score(y_test, y_pred)","score":1,"hint":"r2_score(y_test, y_pred)"},
        {"id":"M11_1","ans":"xgb.XGBRegressor","score":0,"hint":""},
        {"id":"M11_2","ans":"n_estimators=100","score":1,"hint":"n_estimators=100"},
        {"id":"M12","ans":"xgb_model.fit(X_train, y_train)","score":1,"hint":"xgb_model.fit(X_train, y_train)"},
        {"id":"M13","ans":"xgb_model.predict(X_test)","score":1,"hint":"xgb_model.predict(X_test)"},
        {"id":"M14_1","ans":"rf_model.score(X_train, y_train)","score":0,"hint":""},
        {"id":"M14_2","ans":"rf_model.score(X_test, y_test)","score":1,"hint":"test_score"},
        {"id":"M15_1","ans":"mean_squared_error(y_test, y_pred_xgb)","score":0,"hint":""},
        {"id":"M15_2","ans":"r2_score(y_test, y_pred_xgb)","score":1,"hint":"r2_score"},
    ],
    "textItems": [
        {"id":"error_analysis","keywords":["过拟合","欠拟合","误差","分析","错误"],"score":1,"hint":"错误分析"},
        {"id":"improve_suggest","keywords":["增加","调整","优化","改进","特征"],"score":1,"hint":"改进建议"},
    ]
},

# ── 2.2.4 线性回归+XGBoost低碳（20分）
"2.2.4": {
    "max": 20,
    "items": [
        {"id":"M1_1","ans":"pd.read_csv('carbon_data.csv')","score":1,"hint":"read_csv 加载数据"},
        {"id":"M1_2","ans":"data.head()","score":1,"hint":"data.head()"},
        {"id":"M2_1","ans":"data.drop","score":0,"hint":""},
        {"id":"M2_2","ans":"columns","score":1,"hint":"drop(columns=['序号','所用时间'])"},
        {"id":"M3_1","ans":"data_cleaned.drop","score":0,"hint":""},
        {"id":"M3_2","ans":"columns","score":0,"hint":""},
        {"id":"M3_3","ans":"target","score":1,"hint":"columns=target 或 columns=[target]"},
        {"id":"M3_4","ans":"data_cleaned[target]","score":1,"hint":"data_cleaned[target]"},
        {"id":"M4_1","ans":"train_test_split","score":0,"hint":""},
        {"id":"M4_2","ans":"X, y, test_size=0.2","score":1,"hint":"test_size=0.2"},
        {"id":"M5","ans":"LinearRegression()","score":1,"hint":"LinearRegression()"},
        {"id":"M6","ans":"model.fit(X_train, y_train)","score":1,"hint":"model.fit(X_train, y_train)"},
        {"id":"M7","ans":"dump(model, model_filename)","score":1,"hint":"joblib.dump(model, model_filename)"},
        {"id":"M8","ans":"model.predict(X_test)","score":1,"hint":"model.predict(X_test)"},
        {"id":"M9_1","ans":"results.to_csv","score":0,"hint":""},
        {"id":"M9_2","ans":"results_filename","score":1,"hint":"保存预测结果"},
        {"id":"M10_1","ans":"mean_squared_error(y_test, y_pred)","score":1,"hint":"MSE"},
        {"id":"M10_2","ans":"r2_score(y_test, y_pred)","score":1,"hint":"R²"},
        {"id":"M11_1","ans":"XGBRegressor","score":0,"hint":""},
        {"id":"M11_2","ans":"n_estimators=1000, learning_rate=0.05, max_depth=5","score":1,"hint":"超参数"},
        {"id":"M12","ans":"xgb_model.fit(X_train, y_train)","score":1,"hint":"xgb_model.fit(...)"},
        {"id":"M13","ans":"xgb_model.predict(X_test)","score":1,"hint":"xgb_model.predict(X_test)"},
        {"id":"M14_1","ans":"mean_squared_error(y_test, y_pred_xg)","score":0,"hint":""},
        {"id":"M14_2","ans":"r2_score(y_test, y_pred_xg)","score":1,"hint":"XGBoost R²"},
    ],
    "textItems": [
        {"id":"error_analysis","keywords":["过拟合","欠拟合","误差","分析","错误"],"score":1,"hint":"错误分析"},
        {"id":"improve_suggest","keywords":["增加","调整","优化","改进","特征"],"score":1,"hint":"改进建议"},
    ]
},

# ── 2.2.5 决策树（20分）
"2.2.5": {
    "max": 20,
    "items": [
        {"id":"M1_1","ans":"pd.read_csv('fitness_data.csv')","score":1,"hint":"read_csv 加载数据"},
        {"id":"M1_2","ans":"df.head()","score":1,"hint":"df.head()"},
        {"id":"M2_1","ans":"pd.get_dummies","score":1,"hint":"pd.get_dummies(X) 分类转数值"},
        {"id":"M2_2","ans":"df['Your age'].apply(lambda x: int(x.split(' ')[0]))","score":1,"hint":"target变量：apply lambda提取整数年龄"},
        {"id":"M3","ans":"train_test_split","score":0,"hint":""},
        {"id":"M3_param","ans":"X, y, test_size=0.2","score":1,"hint":"test_size=0.2"},
        {"id":"M4","ans":"DecisionTreeRegressor","score":2,"hint":"DecisionTreeRegressor(random_state=42)"},
        {"id":"M5","ans":"dt_model.fit(X_train, y_train)","score":2,"hint":"dt_model.fit(X_train, y_train)"},
        {"id":"M6","ans":"dump(dt_model, model_file)","score":1,"hint":"pickle.dump(dt_model, model_file)"},
        {"id":"M7","ans":"dt_model.predict(X_test)","score":1,"hint":"dt_model.predict(X_test)"},
        {"id":"M8_1","ans":"results.to_csv","score":0,"hint":""},
        {"id":"M8_2","ans":"results_filename","score":1,"hint":"保存预测结果"},
        {"id":"M10","ans":"mean_squared_error(y_test, y_pred)","score":1,"hint":"MSE"},
        {"id":"M11","ans":"mean_absolute_error(y_test, y_pred)","score":1,"hint":"MAE"},
        {"id":"M12","ans":"r2_score(y_test, y_pred)","score":1,"hint":"R²"},
    ],
    "textItems": [
        {"id":"error_analysis","keywords":["过拟合","欠拟合","误差","分析","错误"],"score":1,"hint":"错误分析"},
        {"id":"improve_suggest","keywords":["增加","调整","优化","改进","特征"],"score":1,"hint":"改进建议"},
    ]
},

# ── 3.2.1 ONNX ResNet（18分代码+2分交互=20分）
"3.2.1": {
    "max": 20,
    "items": [
        {"id":"b1","ans":"ort.InferenceSession('resnet.onnx')","score":2,"hint":"ort.InferenceSession('resnet.onnx')"},
        {"id":"b2","ans":"Image.open('img_test.jpg').convert","score":2,"hint":"Image.open('img_test.jpg').convert('RGB')"},
        {"id":"b3","ans":"preprocess_image(image)","score":2,"hint":"preprocess_image(image)"},
        {"id":"b4","ans":"session.run","score":2,"hint":"session.run([output_name], {...})"},
        {"id":"b5","ans":"scipy.special.softmax","score":2,"hint":"scipy.special.softmax(output, axis=-1)"},
        {"id":"b6","ans":"np.argsort(probabilities[0])","score":3,"hint":"np.argsort(probabilities[0])[-5:][::-1]"},
        {"id":"b7","ans":"probabilities[0][top5_idx]","score":3,"hint":"probabilities[0][top5_idx]"},
    ],
    "textItems": [
        {"id":"interactionOpt","keywords":["优化","加载","展示","反馈","结果","用户","交互"],"score":2,"hint":"人机交互优化方式，至少1条"},
    ]
},

# ── 3.2.2 手写数字识别（20分）
"3.2.2": {
    "max": 20,
    "items": [
        {"id":"b1","ans":"onnxruntime.InferenceSession('mnist.onnx')","score":2,"hint":"InferenceSession('mnist.onnx')"},
        {"id":"b2","ans":"Image.open('img_test.png').convert","score":2,"hint":"Image.open('img_test.png').convert('L')"},
        {"id":"b3","ans":"image.resize((28, 28))","score":2,"hint":"image.resize((28, 28))"},
        {"id":"b4","ans":"np.array(image)","score":2,"hint":"np.array(image)"},
        {"id":"b5","ans":"np.expand_dims(image_array, axis=0)","score":2,"hint":"np.expand_dims(image_array, axis=0)"},
        {"id":"b6","ans":"np.expand_dims(image_array, axis=0)","score":2,"hint":"添加通道维度"},
        {"id":"b7","ans":"ort_session.get_inputs()[0].name","score":2,"hint":"ort_session.get_inputs()[0].name"},
        {"id":"b8","ans":"ort_session.run(None, ort_inputs)","score":2,"hint":"ort_session.run(None, ort_inputs)"},
        {"id":"b9","ans":"np.argmax(ort_outs[0])","score":2,"hint":"np.argmax(ort_outs[0])"},
    ],
    "textItems": [
        {"id":"flowNorm","keywords":["加载","预处理","预测","输出","流程","步骤"],"score":2,"hint":"人机交互最优流程"},
    ]
},

# ── 3.2.3 面部表情识别（16分代码+1分交互=17分，用18分）
"3.2.3": {
    "max": 18,
    "items": [
        {"id":"b1","ans":"{'neutral':0,'happiness':1,'surprise':2,'sadness':3,'anger':4,'disgust':5,'fear':6,'contempt':7}","score":3,"hint":"情感映射表字典"},
        {"id":"b2","ans":"ort.InferenceSession('emotion-ferplus.onnx')","score":3,"hint":"ort.InferenceSession('emotion-ferplus.onnx')"},
        {"id":"b3","ans":"preprocess('img_test.png')","score":3,"hint":"preprocess('img_test.png')"},
        {"id":"b4","ans":"ort_session.run(None, ort_inputs)","score":3,"hint":"ort_session.run(None, ort_inputs)"},
        {"id":"b5","ans":"np.argmax(ort_outs[0])","score":3,"hint":"np.argmax(ort_outs[0])"},
        {"id":"b6","ans":"[k for k, v in emotion_table.items() if v == predicted_label][0]","score":3,"hint":"根据索引反查情感名称"},
    ],
    "textItems": [
        {"id":"flowNorm","keywords":["加载","预处理","预测","输出","流程","步骤","情感"],"score":1,"hint":"人机交互最优流程"},
    ]
},

# ── 3.2.4 花朵识别（18分代码+1分交互）
"3.2.4": {
    "max": 18,
    "items": [
        {"id":"b1","ans":"ort.InferenceSession('flower-detection.onnx')","score":2,"hint":"InferenceSession('flower-detection.onnx')"},
        {"id":"b2","ans":"open('labels.txt')","score":2,"hint":"open('labels.txt') as f"},
        {"id":"b3","ans":"Image.open('flower_test.png').convert('RGB')","score":2,"hint":"Image.open('flower_test.png').convert('RGB')"},
        {"id":"b4","ans":"preprocess_image(image)","score":2,"hint":"preprocess_image(image)"},
        {"id":"b5","ans":"session.run([output_name], {input_name: processed_image})[0]","score":2,"hint":"session.run(...)"},
        {"id":"b6","ans":"scipy.special.softmax","score":2,"hint":"scipy.special.softmax(output, axis=-1)"},
        {"id":"b7","ans":"np.argmax(accuracy)","score":2,"hint":"np.argmax(accuracy)"},
        {"id":"b8","ans":"accuracy[0][predicted_idx] * 100","score":2,"hint":"accuracy[0][predicted_idx] * 100"},
        {"id":"b9","ans":"labels[predicted_idx]","score":2,"hint":"labels[predicted_idx]"},
    ],
    "textItems": [
        {"id":"flowNorm","keywords":["加载","预处理","预测","输出","流程","步骤","花朵"],"score":1,"hint":"人机交互最优流程"},
    ]
},

# ── 3.2.5 人脸检测（17分代码+1分交互）
"3.2.5": {
    "max": 18,
    "items": [
        {"id":"b1","ans":"name.strip()","score":2,"hint":"name.strip() 去空白"},
        {"id":"b2","ans":"ort.InferenceSession","score":2,"hint":"ort.InferenceSession('version-RFB-320.onnx')"},
        {"id":"b3","ans":"ort_session.get_inputs","score":2,"hint":"ort_session.get_inputs()[0].name"},
        {"id":"b4","ans":"makedirs(result_path)","score":2,"hint":"os.makedirs(result_path)"},
        {"id":"b5","ans":"cv2.imread(img_path)","score":2,"hint":"cv2.imread(img_path)"},
        {"id":"b6","ans":"cv2.resize","score":2,"hint":"cv2.resize(image, (320, 240))"},
        {"id":"b6_1","ans":"image","score":0,"hint":""},
        {"id":"b7","ans":"np.array","score":2,"hint":"np.array([127, 127, 127])"},
        {"id":"b8","ans":"np.expand_dims","score":1,"hint":"np.expand_dims(image, axis=0)"},
        {"id":"b9","ans":"ort_session.run","score":2,"hint":"ort_session.run(None, {input_name: image})"},
    ],
    "textItems": [
        {"id":"flowNorm","keywords":["加载","检测","输出","流程","步骤","人脸","置信度"],"score":1,"hint":"人机交互最优流程≥3条"},
    ]
},

}

# ══════════════════════════════════════════════════════
# 生成打分 JS 代码片段
# ══════════════════════════════════════════════════════
def gen_scoring_js(qid, config):
    items = config["items"]
    text_items = config.get("textItems", [])
    max_score = config["max"]

    items_json_lines = []
    for it in items:
        hint = it.get("hint", "").replace("\\","\\\\").replace('"','\\"').replace("'","\\'")
        ans  = it["ans"].replace("\\","\\\\").replace('"','\\"')
        items_json_lines.append(
            f'        {{id:"{it["id"]}", ans:"{ans}", score:{it["score"]}, hint:"{hint}"}}'
        )

    text_items_json_lines = []
    for ti in text_items:
        kw_json = str(ti["keywords"]).replace("'", '"')
        hint = ti.get("hint","").replace('"','\\"')
        text_items_json_lines.append(
            f'        {{id:"{ti["id"]}", keywords:{kw_json}, score:{ti["score"]}, hint:"{hint}"}}'
        )

    items_json = ",\n".join(items_json_lines)
    text_items_json = ",\n".join(text_items_json_lines)

    js = f"""
    // ── 打分逻辑（自动注入）──────────────────────────────────
    const QMAX = {max_score};
    function fuzzyMatch(user, correct) {{
        if (!user) return false;
        user = user.trim().toLowerCase().replace(/\\s+/g, '');
        correct = correct.trim().toLowerCase().replace(/\\s+/g, '');
        return user === correct || user.includes(correct) || correct.includes(user);
    }}
    const scoring = [
{items_json}
    ];
    const textScoring = [
{text_items_json}
    ];
    document.getElementById('btnCheck').onclick = function() {{
        let total = 0;
        let wrong = [], right = [];
        scoring.forEach(function(item) {{
            var el = document.getElementById(item.id);
            if (!el) return;
            var val = el.value.trim();
            if (fuzzyMatch(val, item.ans)) {{
                total += item.score;
                right.push('✅ ' + item.id + '：正确 +' + item.score + '分');
            }} else {{
                var entry = '❌ ' + item.id + ' 正确答案：' + item.ans;
                if (item.hint) entry += '<div class="hint-box">💡 提示：' + item.hint + '</div>';
                wrong.push(entry);
            }}
        }});
        textScoring.forEach(function(ti) {{
            var el = document.getElementById(ti.id);
            if (!el) return;
            var val = el.value.trim();
            var hasKw = ti.keywords.some(function(k){{return val.includes(k);}});
            if (val.length >= 15 && hasKw) {{
                total += ti.score;
                right.push('✅ ' + ti.id + '：+' + ti.score + '分');
            }} else {{
                wrong.push('❌ ' + ti.id + '（' + ti.hint + '）：内容不足或缺少关键词');
            }}
        }});
        total = Math.min(total, QMAX);
        var sr = document.getElementById('scoreResult');
        if (sr) {{ sr.style.display = 'block'; sr.innerHTML = '<strong>本次得分：' + total + ' / ' + QMAX + ' 分</strong>'; }}
        var ac = document.getElementById('answerComparison');
        if (ac) {{
            ac.style.display = 'block';
            var wEl = document.getElementById('wrongAnswer');
            var cEl = document.getElementById('correctAnswer');
            if (wEl) wEl.innerHTML = wrong.join('<br>') || '无错误';
            if (cEl) cEl.innerHTML = right.join('<br>') || '全部正确';
        }}
        localStorage.setItem('exam_score_{qid}', total);
        localStorage.setItem('exam_done_{qid}', new Date().toISOString());
    }};
    document.getElementById('btnReset').onclick = function() {{
        document.querySelectorAll('.blank').forEach(function(i){{i.value='';}});
        document.querySelectorAll('.text-answer, textarea').forEach(function(i){{i.value='';}});
        var sr = document.getElementById('scoreResult'); if(sr) sr.style.display='none';
        var ac = document.getElementById('answerComparison'); if(ac) ac.style.display='none';
        localStorage.removeItem('exam_answers_{qid}');
        localStorage.removeItem('exam_score_{qid}');
        localStorage.removeItem('exam_done_{qid}');
    }};
    // 恢复已保存答案
    window.addEventListener('DOMContentLoaded', function() {{
        var saved = localStorage.getItem('exam_answers_{qid}');
        if (saved) {{
            var answers = JSON.parse(saved);
            Object.keys(answers).forEach(function(id) {{
                var el = document.getElementById(id);
                if (el) el.value = answers[id];
            }});
        }}
    }});
    document.querySelectorAll('.blank, textarea').forEach(function(el) {{
        el.addEventListener('input', function() {{
            var answers = {{}};
            document.querySelectorAll('.blank, textarea').forEach(function(e){{ if(e.id) answers[e.id]=e.value; }});
            localStorage.setItem('exam_answers_{qid}', JSON.stringify(answers));
        }});
    }});
    // ─────────────────────────────────────────────────────────
"""
    return js

# ══════════════════════════════════════════════════════
# score/answer div 模板（插到 btnRetry 后面）
# ══════════════════════════════════════════════════════
SCORE_DIV = """
            <div class="score-result" id="scoreResult" style="margin-top:15px;padding:12px;background:#f0fff4;border:1px solid #9ae6b4;border-radius:4px;font-weight:bold;color:#22543d;display:none;"></div>
            <div class="answer-comparison" id="answerComparison" style="margin-top:12px;padding:12px;background:#fff5f5;border:1px solid #fc8181;border-radius:4px;display:none;">
                <div style="font-weight:bold;margin-bottom:8px;color:#c53030;">答案对比</div>
                <div class="wrong-answer" id="wrongAnswer" style="background:#fee;border-left:4px solid #e53e3e;padding:8px;margin-bottom:8px;border-radius:4px;line-height:1.8;"></div>
                <div class="correct-answer" id="correctAnswer" style="background:#e6f9f0;border-left:4px solid #38a169;padding:8px;border-radius:4px;line-height:1.8;"></div>
            </div>"""

# ══════════════════════════════════════════════════════
# 执行修复
# ══════════════════════════════════════════════════════
fixed = []
skipped = []

for qid, config in SCORING_MAP.items():
    html_path = os.path.join(BASE, qid, "index.html")
    if not os.path.exists(html_path):
        print(f"[SKIP] {qid}: file not found")
        skipped.append(qid)
        continue

    content = open(html_path, "r", encoding="utf-8").read()

    # 检查是否已有打分逻辑
    if "btnCheck').onclick" in content or 'btnCheck").onclick' in content:
        print(f"[SKIP] {qid}: already has scoring logic")
        skipped.append(qid)
        continue

    # 1. 在 btnRetry 按钮后插入 score/answer div（找 </script> 前的 analysisBox div 后面）
    # 寻找 analysisBox div 结束后的 <script> 标签位置
    # 策略：在 id="analysisContent"></div>\n</div>\n<script> 模式前插入
    if 'id="scoreResult"' not in content:
        # 找到 analysisBox 区域后面的 <script> 标签
        # 替换策略：在 <script>\n        const QID 前插入
        script_marker = '<script>\n        const QID'
        if script_marker not in content:
            script_marker = '<script>\n        const QID = "' + qid + '"'
        if script_marker in content:
            content = content.replace(script_marker, SCORE_DIV + '\n' + script_marker, 1)
        else:
            print(f"[WARN] {qid}: cannot find script marker, trying alternate")
            # 备用：找 <script> 并在前插入
            alt_marker = f'<script>\n        const QID = "{qid}"'
            if alt_marker in content:
                content = content.replace(alt_marker, SCORE_DIV + '\n' + alt_marker, 1)
            else:
                print(f"[ERROR] {qid}: cannot insert score divs")
                skipped.append(qid)
                continue

    # 2. 在 </script> 前插入打分 JS
    scoring_js = gen_scoring_js(qid, config)
    # 找到最后的 </script>
    last_script_end = content.rfind('</script>')
    if last_script_end == -1:
        print(f"[ERROR] {qid}: no </script> found")
        skipped.append(qid)
        continue

    content = content[:last_script_end] + scoring_js + '\n</script>' + content[last_script_end+9:]

    # 3. 更新 QMAX
    content = re.sub(r'const QMAX\s*=\s*0;', f'// QMAX set in scoring block', content)

    open(html_path, "w", encoding="utf-8").write(content)
    fixed.append(qid)
    print(f"[FIXED] {qid}")

print(f"\n=== 完成 ===")
print(f"已修复({len(fixed)}): {fixed}")
print(f"已跳过({len(skipped)}): {skipped}")
