import 'database_provider.dart';
import '../models/.dart';

class MasterTipeKamarRepository {
  Future<List<MasterTipeKamar>> getAllData({String? query, String orderBy = 'id DESC', int? limit}) async {
    final db = await DatabaseProvider().database;
    List<Map<String, dynamic>> maps;
    if (query != null && query.trim().isNotEmpty) {
      maps = await db.query(
        'master_tipe_kamar',
        where: 'nama_tipe LIKE ?',
        whereArgs: ['%${query.trim()}%'],
        orderBy: orderBy,
        limit: limit,
      );
    } else {
      maps = await db.query('master_tipe_kamar', orderBy: orderBy, limit: limit);
    }
    return maps.map((map) => MasterTipeKamar.fromMap(map)).toList();
  }

  Future<void> insert(MasterTipeKamar mastertipekamar) async {
    final db = await DatabaseProvider().database;
    final data = mastertipekamar.toMap();
    data.remove('id');
    await db.insert('master_tipe_kamar', data);
  }

  Future<void> update(MasterTipeKamar mastertipekamar) async {
    final db = await DatabaseProvider().database;
    final data = mastertipekamar.toMap();
    await db.update(
      'master_tipe_kamar',
      data,
      where: 'id = ?',
      whereArgs: [mastertipekamar.id],
    );
  }

  Future<void> delete(String id) async {
    final db = await DatabaseProvider().database;
    await db.delete('master_tipe_kamar', where: 'id = ?', whereArgs: [id]);
  }

  Future<void> import(List<MasterTipeKamar> mastertipekamars) async {
    final db = await DatabaseProvider().database;
    final batch = db.batch();
    for (final mastertipekamar in mastertipekamars) {
      final data = mastertipekamar.toMap();
      data.remove('id');
      batch.insert('master_tipe_kamar', data);
    }
    await batch.commit(noResult: true);
  }

  Future<List<Map<String, dynamic>>> getPivotData() async {
    final db = await DatabaseProvider().database;
    final result = await db.rawQuery('''
      SELECT judul, DATE(date_column) AS date, COUNT(judul) AS count
      FROM master_tipe_kamar
      GROUP BY judul, DATE(date_column)
    ''');
    return result;
  }
}