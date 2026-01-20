import { CloudUpload, Download, FolderCog } from 'lucide-react';

export function FeatureSection() {
  const features = [
    {
      icon: <CloudUpload size={32} />,
      title: 'Tải lên & Tải xuống',
      desc: 'Tải lên tệp lên bộ nhớ đám mây và tải xuống bất cứ lúc nào, bất cứ nơi đâu.',
    },
    {
      icon: <FolderCog size={32} />,
      title: 'Quản lý tập tin',
      desc: 'Tổ chức, đổi tên, xóa và quản lý tất cả các tệp của bạn một cách dễ dàng.',
    },
    {
      icon: <Download size={32} />,
      title: 'Kiến trúc đám mây',
      desc: 'Được xây dựng trên nền tảng đám mây để đảm bảo tính sẵn sàng và mở rộng linh hoạt.',
    },
  ];

  return (
    <>
      {' '}
      <section className="bg-[#020617] py-24">
        <div className="max-w-6xl mx-auto px-6 grid md:grid-cols-3 gap-8">
          {features.map((f, i) => (
            <div
              key={i}
              className="bg-white/5 border border-white/10 rounded-2xl p-6 text-white hover:scale-105 transition"
            >
              <div className="text-cyan-300 mb-4">{f.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{f.title}</h3>
              <p className="text-white/70 text-sm">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>
    </>
  );
}
