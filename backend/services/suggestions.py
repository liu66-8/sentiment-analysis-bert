from backend.services.predictor import LABEL_DISPLAY_NAMES, LABEL_CATEGORIES, LABEL_MAP


SUGGESTION_RULES = {
    'location_traffic_convenience': {
        'header': '🚗 交通便利性',
        '负面': '建议在店铺宣传中提供详细的交通路线指引（地铁/公交），并考虑与导航平台合作标注准确位置。',
        '中性': '可进一步加强交通指引宣传，如在地图和点评平台明确标注最近地铁站和公交线路。',
        '正面': '交通便利是优势，可在宣传中突出"交通便捷"标签吸引更多顾客。',
    },
    'location_distance_from_business_district': {
        'header': '📍 商圈位置',
        '负面': '建议在周边商圈/写字楼投放宣传物料，或提供外卖服务以弥补位置劣势。',
        '中性': '位置尚可但非核心商圈，可通过特色菜品或主题活动吸引顾客专程前来。',
        '正面': '位于核心商圈是巨大优势，建议保持并利用流量红利。',
    },
    'location_easy_to_find': {
        'header': '🔍 寻店便利性',
        '负面': '建议在显眼位置增设招牌和指示牌，优化线上地图定位，降低顾客寻找难度。',
        '中性': '可增设路边指引标识，并在预订短信中附带详细路线说明。',
        '正面': '店铺容易被找到，继续保持清晰的标识系统。',
    },
    'service_wait_time': {
        'header': '⏰ 排队等待',
        '负面': '排队时间过长严重影响体验。建议引入线上取号系统、增加等位区舒适度、提供等位小食。',
        '中性': '可优化出餐流程，高峰时段适当增加人手，缩短顾客等待时间。',
        '正面': '出餐效率高，继续保持高效的运营管理。',
    },
    'service_waiters_attitude': {
        'header': '👩‍🍳 服务态度',
        '负面': '服务态度是餐饮业核心。建议加强员工服务培训、建立考核激励机制、定期收集顾客反馈。',
        '中性': '建议定期组织服务礼仪培训，提升员工主动服务意识，可设立服务之星评选。',
        '正面': '服务态度优秀是核心竞争力，建议继续保持并推广为品牌特色。',
    },
    'service_parking_convenience': {
        'header': '🅿️ 停车便利性',
        '负面': '建议与周边停车场合作提供停车优惠，或在宣传中标注最近停车场信息。',
        '中性': '可提供代客泊车服务或与附近停车场谈合作折扣。',
        '正面': '停车方便是加分项，可在对外宣传中强调。',
    },
    'service_serving_speed': {
        'header': '🍽️ 上菜速度',
        '负面': '上菜慢会极大影响用餐体验。建议优化厨房动线、预制半成品、高峰时段增加厨师。',
        '中性': '可进一步优化备餐流程，减少顾客等餐焦虑（如上餐前小食）。',
        '正面': '上菜速度快，说明厨房管理高效，请保持这一优势。',
    },
    'price_level': {
        'header': '💵 价格水平',
        '负面': '若价格偏高但体验不匹配，需重新评估定价策略或提升品质感以匹配价位。',
        '中性': '价格适中，可考虑推出不同档位套餐，满足多层次消费需求。',
        '正面': '价格合理/亲民，建议继续保持并作为核心卖点宣传。',
    },
    'price_cost_effective': {
        'header': '💰 性价比',
        '负面': '性价比低是顾客流失主因。建议调整菜品份量或价格，增加套餐组合提升价值感。',
        '中性': '性价比尚可，可通过推出特价菜/午市套餐进一步提升竞争力。',
        '正面': '高性价比是回头客的关键，建议保持并做为重点营销方向。',
    },
    'price_discount': {
        'header': '🎫 优惠力度',
        '负面': '建议增设会员体系、节假日优惠、团购套餐等，吸引价格敏感型顾客。',
        '中性': '可定期推出限时优惠活动，增加消费吸引力。',
        '正面': '优惠活动丰富，继续保持灵活的促销策略。',
    },
    'environment_decoration': {
        'header': '🎨 装修风格',
        '负面': '环境陈旧或风格不佳会降低消费体验。建议进行局部翻新、改善灯光氛围、突出主题风格。',
        '中性': '装修尚可但缺乏特色，可考虑融入网红元素或特定主题风格增强记忆点。',
        '正面': '装修风格受到好评，可鼓励顾客拍照分享，形成社交传播。',
    },
    'environment_noise': {
        'header': '🔊 环境噪音',
        '负面': '噪音过大影响用餐体验。建议增加吸音装饰、优化餐桌间距、设立安静用餐区。',
        '中性': '可在特定时段控制背景音乐音量，为顾客营造更舒适的就餐环境。',
        '正面': '环境安静舒适，适合商务宴请或约会场景，可加强此类场景营销。',
    },
    'environment_space': {
        'header': '📐 空间大小',
        '负面': '空间狭小影响舒适度。建议优化桌椅布局、运用镜面增加空间感、提供包厢预约。',
        '中性': '空间尚可接受，可通过合理布局和装饰进一步提升空间利用率。',
        '正面': '空间宽敞受到好评，适合家庭聚餐和团体活动。',
    },
    'environment_cleaness': {
        'header': '🧹 卫生状况',
        '负面': '卫生问题是餐饮业的红线！建议立即加强清洁管理、建立卫生检查制度、公开透明后厨。',
        '中性': '建议进一步提升卫生标准，做到明厨亮灶，增强顾客信任感。',
        '正面': '环境卫生优秀，建议保持高标准并作为品牌亮点宣传。',
    },
    'dish_portion': {
        'header': '⚖️ 菜品分量',
        '负面': '分量不足是常见投诉点。建议适当增加主料份量、提供大小份选择、优化摆盘视觉。',
        '中性': '份量中规中矩，可考虑推出加量版或分享装满足不同需求。',
        '正面': '分量充足受到好评，继续保持并可作为卖点。',
    },
    'dish_taste': {
        'header': '👅 菜品口味',
        '负面': '口味是餐厅的生命线！建议立即调整配方、更换厨师或进行口味调研，挽救核心体验。',
        '中性': '建议在保持现有水准基础上研发特色菜品，打造招牌菜系。',
        '正面': '口味出众是餐厅核心优势，建议持续创新保持食客新鲜感。',
    },
    'dish_look': {
        'header': '📸 菜品外观',
        '负面': '菜品颜值影响社交分享意愿。建议提升摆盘艺术性、使用精美器皿、注重色彩搭配。',
        '中性': '可邀请专业摆盘培训，提升菜品视觉吸引力，激发顾客拍照分享。',
        '正面': '菜品外观精美，适合社交媒体传播，建议鼓励顾客打卡分享。',
    },
    'dish_recommendation': {
        'header': '⭐ 推荐意愿',
        '负面': '顾客不愿推荐说明存在严重问题。建议深入调研不满原因，从核心体验入手系统性改进。',
        '中性': '建议通过会员推荐奖励机制、好评返券等方式提升推荐意愿。',
        '正面': '顾客愿意推荐是最佳口碑，建议设置推荐奖励体系放大口碑效应。',
    },
    'others_overall_experience': {
        'header': '🌟 整体体验',
        '负面': '整体体验不佳需全面复盘。建议从服务、菜品、环境三个维度制定改善计划并跟踪进度。',
        '中性': '整体体验尚可但缺乏惊喜，可设计特色体验环节（如互动菜品、节日活动）提升记忆点。',
        '正面': '顾客整体体验优秀，建议持续关注各维度变化，保持高品质水准。',
    },
    'others_willing_to_consume_again': {
        'header': '🔁 复购意愿',
        '负面': '低复购意愿反映深层次问题。建议推出会员储值优惠、定期新品推送、建立顾客社群。',
        '中性': '可通过会员积分制度、老客专属优惠、定期回访等方式提升复购率。',
        '正面': '高复购意愿说明顾客忠诚度高，建议建立会员体系深度运营忠实顾客。',
    },
}


CATEGORY_KEYWORDS = {
    '位置': ['交通', '位置', '商圈', '找到'],
    '服务': ['服务', '排队', '上菜', '停车', '态度', '等待'],
    '价格': ['价格', '性价比', '优惠', '折扣'],
    '环境': ['装修', '环境', '噪音', '空间', '卫生', '干净'],
    '菜品': ['口味', '分量', '外观', '推荐', '菜品'],
    '整体': ['体验', '复购', '再来'],
}


def generate_suggestions(predictions, summary):
    pos_count = summary.get('正面', 0)
    neg_count = summary.get('负面', 0)
    neu_count = summary.get('中性', 0)
    total = pos_count + neg_count + neu_count + summary.get('未提及', 0)

    overall = _build_overall(pos_count, neg_count, neu_count, total)

    category_advice = _build_category_advice(predictions)

    dim_details = []
    for key, val in predictions.items():
        sent = val.get('sentiment', '未提及')
        if sent in ('负面', '中性'):
            rule = SUGGESTION_RULES.get(key, {})
            header = rule.get('header', val.get('display_name', key))
            advice = rule.get(sent, '')
            if advice:
                dim_details.append({
                    'dimension': key,
                    'display_name': val.get('display_name', key),
                    'header': header,
                    'sentiment': sent,
                    'advice': advice,
                    'priority': 'high' if sent == '负面' else 'medium',
                })

    dim_details.sort(key=lambda x: (0 if x['priority'] == 'high' else 1))

    return {
        'overall': overall,
        'category_advice': category_advice,
        'dim_details': dim_details,
        'strengths': _extract_strengths(predictions),
    }


def _build_overall(pos_count, neg_count, neu_count, total):
    if total == 0:
        return {'level': 'unknown', 'emoji': '🤔', 'title': '暂无数据', 'description': '', 'advice': ''}

    pos_ratio = pos_count / total if total > 0 else 0
    neg_ratio = neg_count / total if total > 0 else 0

    if pos_ratio >= 0.7 and neg_ratio <= 0.1:
        return {
            'level': 'excellent',
            'emoji': '🏆',
            'title': '非常满意 - 综合评价优秀',
            'description': f'{total} 个评价维度中，正面占比 {pos_count}/{total}，负面仅 {neg_count}/{total}。顾客整体满意度很高。',
            'advice': '继续保持现有优势，重点关注少量中性评价维度进行微调优化，防止满意度下滑。建议利用好评进行口碑营销。',
        }
    elif pos_ratio >= 0.5 and neg_ratio <= 0.2:
        return {
            'level': 'good',
            'emoji': '👍',
            'title': '比较满意 - 整体体验良好',
            'description': f'正面评价 {pos_count}/{total}，负面评价 {neg_count}/{total}。整体表现不错，仍有提升空间。',
            'advice': '在保持优势的同时，针对负面和中性维度制定改善计划，逐步提升整体满意度至优秀水平。',
        }
    elif neg_ratio >= 0.4:
        return {
            'level': 'poor',
            'emoji': '⚠️',
            'title': '需要改善 - 负面评价较多',
            'description': f'负面评价 {neg_count}/{total}，顾客体验存在明显问题，需要引起重视。',
            'advice': '建议从负面维度入手，制定优先级改进计划。重点关注高频负面维度，必要时进行深度顾客调研定位根因。',
        }
    else:
        return {
            'level': 'normal',
            'emoji': '📈',
            'title': '有待提升 - 体验中规中矩',
            'description': f'正面 {pos_count}/{total}、中性 {neu_count}/{total}、负面 {neg_count}/{total}。各项指标较为平均。',
            'advice': '在消除负面评价的同时，着力将中性评价转化为正面评价，通过亮点打造提升整体顾客满意度。',
        }


def _build_category_advice(predictions):
    cat_sentiments = {}
    for key, val in predictions.items():
        cat = val.get('category', '其他')
        sent = val.get('sentiment', '未提及')
        if cat not in cat_sentiments:
            cat_sentiments[cat] = {'正面': 0, '中性': 0, '负面': 0, '未提及': 0}
        cat_sentiments[cat][sent] = cat_sentiments[cat].get(sent, 0) + 1

    category_advice = []
    for cat, counts in cat_sentiments.items():
        total_cat = sum(counts.values())
        neg_cat = counts.get('负面', 0)
        neu_cat = counts.get('中性', 0)
        pos_cat = counts.get('正面', 0)

        if neg_cat >= 2:
            advice = f"「{cat}」方面负面评价较多（{neg_cat}/{total_cat}），建议优先改善。"
            emoji = '🔴'
        elif pos_cat > neg_cat + neu_cat:
            advice = f"「{cat}」方面表现优秀（正面 {pos_cat}/{total_cat}），是核心优势，建议继续保持。"
            emoji = '🟢'
        elif neu_cat >= 2:
            advice = f"「{cat}」方面以中性评价为主（{neu_cat}/{total_cat}），有一定提升空间，可优化以形成竞争力。"
            emoji = '🟡'
        else:
            continue

        category_advice.append({'category': cat, 'emoji': emoji, 'advice': advice})

    return category_advice


def _extract_strengths(predictions):
    strengths = []
    for key, val in predictions.items():
        if val.get('sentiment') == '正面':
            strengths.append({
                'dimension': key,
                'display_name': val.get('display_name', key),
                'category': val.get('category', '其他'),
            })

    cat_order = ['位置', '服务', '价格', '环境', '菜品', '整体']
    strengths.sort(key=lambda x: (cat_order.index(x['category']) if x['category'] in cat_order else 99))
    return strengths
