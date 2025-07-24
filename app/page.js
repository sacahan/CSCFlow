import DataSourceList from './components/DataSourceList';

export default function Home() {
    return (
        <main className="container mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold underline">運動中心即時人流監測</h1>
            <DataSourceList />
        </main>
    );
}
